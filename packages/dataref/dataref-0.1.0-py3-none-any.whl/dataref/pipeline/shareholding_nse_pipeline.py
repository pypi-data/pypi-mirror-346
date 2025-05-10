import json
import pandas as pd
import os
import logging
import re
from datetime import datetime
from bs4 import BeautifulSoup
from multiprocessing import Pool
import sys
from pathlib import Path

class ShareholdingNseXbrlExtractor:
    """Class to extract shareholding data from NSE XBRL files efficiently."""
    
    def __init__(self, project_root, config_path="config/shareholding_nse_config.json"):
        """Initialize the extractor with project root and setup logging."""
        self.project_root = Path(project_root).resolve()
        self.log_dir = self.project_root / "logs"
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup logging
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.handlers = []
        file_handler = logging.FileHandler(self.log_dir / "shareholding_nse_xbrl_extract.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(file_handler)
        self.logger = logger
        
        # Load configuration
        config_path = self.project_root / config_path
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Config file not found at {config_path}")
            raise
        
        self.xbrl_tags = self.config["xbrl_tags"]["equity"]["shareholding"]
        
        # Define column orders
        self.column_orders = {
            "main": ["File", "Date", "CompanyName", "Ticker"] + 
                    [field for field in self.xbrl_tags["metadata"] if field != "contextRef"] + 
                    [field for field in self.xbrl_tags["main"] if field != "contextRef"] + ["Subtype"],
            "huf": ["File", "Date", "CompanyName", "Ticker"] + 
                   [field for field in self.xbrl_tags["huf"] if field != "contextRef"] + ["Subtype"],
            "fii": ["Date", "Ticker", "CompanyName", "Name of Shareholder", "Total nos. shares held", "Shareholding %"],
            "dii": ["Date", "Ticker", "CompanyName", "Name of Shareholder", "Total nos. shares held", "Shareholding %"],
            "dii_details": ["Date", "Ticker", "CompanyName", "Category", "Shareholder Name", "Total nos. shares held", "Shareholding %"],
            "fii_details": ["Date", "Ticker", "CompanyName", "Category", "Shareholder Name", "Total nos. shares held", "Shareholding %"]
        }
        self.prefixes = ["in-bse-shp:", ""]

    def process_xbrl_file(self, file_path):
        """Process a single XBRL file in one pass, extracting all data."""
        try:
            # Read and parse the file once
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "lxml-xml")

            main_data = {}
            huf_data = []
            fii_data = []
            dii_data = []
            dii_details_data = []
            fii_details_data = []
            end_date = None

            # Extract date
            for context in soup.find_all("xbrli:context"):
                period = context.find("xbrli:endDate") or context.find("xbrli:instant")
                if period and period.text:
                    try:
                        end_date = datetime.strptime(period.text, "%Y-%m-%d").date()
                        break
                    except ValueError:
                        pass

            # Extract metadata
            name_tag = soup.find("in-bse-shp:NameOfTheCompany", {"contextRef": "OneD"})
            main_data["CompanyName"] = name_tag.text.strip() if name_tag else os.path.basename(os.path.dirname(file_path))
            ticker_tag = soup.find("in-bse-shp:Symbol", {"contextRef": "OneD"})
            main_data["Ticker"] = ticker_tag.text.strip() if ticker_tag else "Unknown"
            main_data["File"] = os.path.basename(file_path)
            main_data["Date"] = end_date.strftime("%Y-%m-%d") if end_date else "Unknown"
            main_data["Subtype"] = "shareholding"

            # Extract main data
            for category, fields in self.xbrl_tags.items():
                if category in ["metadata", "huf", "fii", "dii", "dii_details", "fii_details"]:
                    continue
                for field_name, field_config in fields.items():
                    if field_name == "contextRef":
                        continue
                    tag_list = field_config.get("tag", []) if isinstance(field_config, dict) else field_config
                    context_refs = field_config.get("contextRef", []) if isinstance(field_config, dict) else self.xbrl_tags[category].get("contextRef", [])
                    for tag in tag_list:
                        for prefix in self.prefixes:
                            full_tag = prefix + tag
                            elements = soup.find_all(full_tag)
                            for element in elements:
                                if element.has_attr("contextRef") and any(re.search(ctx, element["contextRef"]) for ctx in context_refs):
                                    value = element.text.strip()
                                    try:
                                        if field_name not in ["CompanyName", "Ticker"]:
                                            main_data[field_name] = float(value.replace(",", "")) if "," in value else float(value)
                                        else:
                                            main_data[field_name] = value
                                    except ValueError:
                                        main_data[field_name] = value
                                    break
                        if field_name in main_data:
                            break

            # Extract HUF data
            huf_context_pattern = r"DetailsSharesHeldByIndividualsOrHUF(\d+)[DI]"
            huf_contexts = {context.get("id"): context for context in soup.find_all("xbrli:context") 
                           if re.match(huf_context_pattern, context.get("id", ""))}
            context_pairs = {}
            for context_id in huf_contexts:
                match = re.match(huf_context_pattern, context_id)
                if match:
                    num = match.group(1)
                    if num not in context_pairs:
                        context_pairs[num] = {"D": None, "I": None}
                    context_pairs[num][context_id[-1]] = context_id

            for num, pair in context_pairs.items():
                huf_entry = {
                    "File": main_data["File"], "Date": main_data["Date"], "CompanyName": main_data["CompanyName"],
                    "Ticker": main_data["Ticker"], "Name": None, "Category": "Promoter Group",
                    "Shares Held": None, "Percentage Held": None, "Shares in Demat Form": None, "Subtype": "huf"
                }
                if pair["D"]:
                    for field_name, tag_list in self.xbrl_tags["huf"].items():
                        if field_name != "Name" or field_name == "contextRef":
                            continue
                        for tag in tag_list:
                            for prefix in self.prefixes:
                                element = soup.find(prefix + tag, {"contextRef": pair["D"]})
                                if element and element.text.strip():
                                    huf_entry["Name"] = element.text.strip()
                                    break
                            if huf_entry["Name"]:
                                break
                if pair["I"]:
                    for field_name, tag_list in self.xbrl_tags["huf"].items():
                        if field_name not in ["Shares Held", "Percentage Held", "Shares in Demat Form"]:
                            continue
                        for tag in tag_list:
                            for prefix in self.prefixes:
                                element = soup.find(prefix + tag, {"contextRef": pair["I"]})
                                if element and element.text.strip():
                                    value = element.text.strip()
                                    try:
                                        huf_entry[field_name] = float(value.replace(",", "")) if "," in value else float(value)
                                    except ValueError:
                                        huf_entry[field_name] = value
                                    break
                            if huf_entry[field_name] is not None:
                                break
                if huf_entry["Name"] or any(huf_entry[field] for field in ["Shares Held", "Percentage Held", "Shares in Demat Form"]):
                    huf_data.append(huf_entry)

            # Extract FII/DII data
            for category, cat_name in [("fii", "FII"), ("dii", "DII")]:
                context_refs = self.xbrl_tags[category].get("contextRef", [])
                for context_ref in context_refs:
                    entry = {
                        "Date": main_data["Date"], "Ticker": main_data["Ticker"], "CompanyName": main_data["CompanyName"],
                        "Name of Shareholder": context_ref, "Total nos. shares held": None, "Shareholding %": None, "File": main_data["File"]
                    }
                    for field_name, tag_list in self.xbrl_tags[category].items():
                        if field_name == "contextRef":
                            continue
                        for tag in tag_list:
                            for prefix in self.prefixes:
                                element = soup.find(prefix + tag, {"contextRef": context_ref})
                                if element and element.text.strip():
                                    value = element.text.strip()
                                    try:
                                        if field_name == "Shareholding percentage":
                                            entry["Shareholding %"] = float(value.replace(",", "")) if "," in value else float(value)
                                        elif field_name == "Total nos. shares held":
                                            entry["Total nos. shares held"] = float(value.replace(",", "")) if "," in value else float(value)
                                    except ValueError:
                                        entry[field_name if field_name != "Shareholding percentage" else "Shareholding %"] = value
                                    break
                            if entry.get("Shareholding %") is not None or entry.get("Total nos. shares held") is not None:
                                break
                    if entry["Total nos. shares held"] is not None or entry["Shareholding %"] is not None:
                        (fii_data if category == "fii" else dii_data).append(entry)

            # Extract DII details
            context_refs = self.xbrl_tags["dii_details"].get("contextRef", [])
            for category_name, fields in self.xbrl_tags["dii_details"].items():
                if category_name in ["contextRef", "Mutual Funds Companies List", "Insurance Companies List"]:
                    continue
                context_ref = fields.get("contextRef", [None])[0]
                if context_ref and any(re.search(ctx, context_ref) for ctx in context_refs):
                    entry = {
                        "Date": main_data["Date"], "Ticker": main_data["Ticker"], "CompanyName": main_data["CompanyName"],
                        "Category": category_name, "Shareholder Name": None, "Total nos. shares held": None,
                        "Shareholding %": None, "File": main_data["File"]
                    }
                    for field_name, tag_list in fields.items():
                        if field_name == "contextRef":
                            continue
                        for tag in tag_list:
                            for prefix in self.prefixes:
                                element = soup.find(prefix + tag, {"contextRef": context_ref})
                                if element and element.text.strip():
                                    value = element.text.strip()
                                    try:
                                        if field_name in ["Total nos. shares held", "Shareholding %"]:
                                            entry[field_name] = float(value.replace(",", "")) if "," in value else float(value)
                                        else:
                                            entry[field_name] = value
                                    except ValueError:
                                        entry[field_name] = value
                                    break
                            if entry.get(field_name):
                                break
                    if entry["Total nos. shares held"] is not None or entry["Shareholding %"] is not None:
                        entry["Shareholder Name"] = entry.get("Shareholder Name", category_name)
                        dii_details_data.append(entry)

            # Extract DII shareholder lists
            for list_name, fields in [("Mutual Funds Companies List", self.xbrl_tags["dii_details"]["Mutual Funds Companies List"]),
                                     ("Insurance Companies List", self.xbrl_tags["dii_details"]["Insurance Companies List"])]:
                context_pattern = fields.get("contextRef", [None])[0]
                contexts = {context.get("id"): context for context in soup.find_all("xbrli:context") 
                           if re.match(context_pattern, context.get("id", ""))}
                context_pairs = {}
                for context_id in contexts:
                    match = re.match(r"(.+)(\d+)[DI]", context_id)
                    if match:
                        num = match.group(2)
                        if num not in context_pairs:
                            context_pairs[num] = {"D": None, "I": None}
                        context_pairs[num][context_id[-1]] = context_id
                for num, pair in context_pairs.items():
                    entry = {
                        "Date": main_data["Date"], "Ticker": main_data["Ticker"], "CompanyName": main_data["CompanyName"],
                        "Category": list_name, "Shareholder Name": None, "Total nos. shares held": None,
                        "Shareholding %": None, "File": main_data["File"]
                    }
                    if pair["D"]:
                        for field_name, tag_list in fields.items():
                            if field_name != "Name" or field_name == "contextRef":
                                continue
                            for tag in tag_list:
                                for prefix in self.prefixes:
                                    element = soup.find(prefix + tag, {"contextRef": pair["D"]})
                                    if element and element.text.strip():
                                        entry["Shareholder Name"] = element.text.strip()
                                        break
                                if entry["Shareholder Name"]:
                                    break
                    if pair["I"]:
                        for field_name, tag_list in fields.items():
                            if field_name not in ["Total nos. shares held", "Shareholding %"]:
                                continue
                            for tag in tag_list:
                                for prefix in self.prefixes:
                                    element = soup.find(prefix + tag, {"contextRef": pair["I"]})
                                    if element and element.text.strip():
                                        value = element.text.strip()
                                        try:
                                            entry[field_name] = float(value.replace(",", "")) if "," in value else float(value)
                                        except ValueError:
                                            entry[field_name] = value
                                        break
                                if entry[field_name] is not None:
                                    break
                    if entry["Shareholder Name"] or entry["Total nos. shares held"] or entry["Shareholding %"]:
                        entry["Shareholder Name"] = entry.get("Shareholder Name", list_name)
                        dii_details_data.append(entry)

            # Extract FII details
            context_refs = self.xbrl_tags["fii_details"].get("contextRef", [])
            for category_name, fields in self.xbrl_tags["fii_details"].items():
                if category_name in ["contextRef", "Foreign Portfolio Investors Category I list"]:
                    continue
                context_ref = fields.get("contextRef", [None])[0]
                if context_ref and any(re.search(ctx, context_ref) for ctx in context_refs):
                    entry = {
                        "Date": main_data["Date"], "Ticker": main_data["Ticker"], "CompanyName": main_data["CompanyName"],
                        "Category": category_name, "Shareholder Name": None, "Total nos. shares held": None,
                        "Shareholding %": None, "File": main_data["File"]
                    }
                    for field_name, tag_list in fields.items():
                        if field_name == "contextRef":
                            continue
                        for tag in tag_list:
                            for prefix in self.prefixes:
                                element = soup.find(prefix + tag, {"contextRef": context_ref})
                                if element and element.text.strip():
                                    value = element.text.strip()
                                    try:
                                        if field_name in ["Total nos. shares held", "Shareholding %"]:
                                            entry[field_name] = float(value.replace(",", "")) if "," in value else float(value)
                                        else:
                                            entry[field_name] = value
                                    except ValueError:
                                        entry[field_name] = value
                                    break
                            if entry.get(field_name):
                                break
                    if entry["Total nos. shares held"] is not None or entry["Shareholding %"] is not None:
                        entry["Shareholder Name"] = entry.get("Shareholder Name", category_name)
                        fii_details_data.append(entry)

            # Extract FII shareholder lists
            for list_name, fields in [("Foreign Portfolio Investors Category I list", self.xbrl_tags["fii_details"]["Foreign Portfolio Investors Category I list"])]:
                context_pattern = fields.get("contextRef", [None])[0]
                contexts = {context.get("id"): context for context in soup.find_all("xbrli:context") 
                           if re.match(context_pattern, context.get("id", ""))}
                context_pairs = {}
                for context_id in contexts:
                    match = re.match(r"(.+)(\d+)[DI]", context_id)
                    if match:
                        num = match.group(2)
                        if num not in context_pairs:
                            context_pairs[num] = {"D": None, "I": None}
                        context_pairs[num][context_id[-1]] = context_id
                for num, pair in context_pairs.items():
                    entry = {
                        "Date": main_data["Date"], "Ticker": main_data["Ticker"], "CompanyName": main_data["CompanyName"],
                        "Category": list_name, "Shareholder Name": None, "Total nos. shares held": None,
                        "Shareholding %": None, "File": main_data["File"]
                    }
                    if pair["D"]:
                        for field_name, tag_list in fields.items():
                            if field_name != "Name" or field_name == "contextRef":
                                continue
                            for tag in tag_list:
                                for prefix in self.prefixes:
                                    element = soup.find(prefix + tag, {"contextRef": pair["D"]})
                                    if element and element.text.strip():
                                        entry["Shareholder Name"] = element.text.strip()
                                        break
                                if entry["Shareholder Name"]:
                                    break
                    if pair["I"]:
                        for field_name, tag_list in fields.items():
                            if field_name not in ["Total nos. shares held", "Shareholding %"]:
                                continue
                            for tag in tag_list:
                                for prefix in self.prefixes:
                                    element = soup.find(prefix + tag, {"contextRef": pair["I"]})
                                    if element and element.text.strip():
                                        value = element.text.strip()
                                        try:
                                            entry[field_name] = float(value.replace(",", "")) if "," in value else float(value)
                                        except ValueError:
                                            entry[field_name] = value
                                        break
                                if entry[field_name] is not None:
                                    break
                    if entry["Shareholder Name"] or entry["Total nos. shares held"] or entry["Shareholding %"]:
                        entry["Shareholder Name"] = entry.get("Shareholder Name", list_name)
                        fii_details_data.append(entry)

            return main_data, huf_data, fii_data, dii_data, dii_details_data, fii_details_data
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            return None, None, None, None, None, None

    def save_batch_data(self, batch_data, output_folder, timestamp):
        """Append batch data to single CSV files."""
        main_data, huf_data, fii_data, dii_data, dii_details_data, fii_details_data = batch_data

        if main_data:
            main_df = pd.DataFrame(main_data)
            main_df = main_df.reindex(columns=self.column_orders["main"])
            main_df.to_csv(output_folder / f"shareholding_main_{timestamp}.csv", mode='a', 
                          header=not (output_folder / f"shareholding_main_{timestamp}.csv").exists(), index=False)

        if huf_data:
            huf_df = pd.DataFrame(huf_data)
            huf_df = huf_df.reindex(columns=self.column_orders["huf"])
            huf_df.to_csv(output_folder / f"HUF_{timestamp}.csv", mode='a', 
                         header=not (output_folder / f"HUF_{timestamp}.csv").exists(), index=False)

        if fii_data:
            fii_df = pd.DataFrame(fii_data)
            fii_df = fii_df.reindex(columns=self.column_orders["fii"])
            fii_df.to_csv(output_folder / f"FII_{timestamp}.csv", mode='a', 
                         header=not (output_folder / f"FII_{timestamp}.csv").exists(), index=False)

        if dii_data:
            dii_df = pd.DataFrame(dii_data)
            dii_df = dii_df.reindex(columns=self.column_orders["dii"])
            dii_df.to_csv(output_folder / f"DII_{timestamp}.csv", mode='a', 
                         header=not (output_folder / f"DII_{timestamp}.csv").exists(), index=False)

        if dii_details_data:
            dii_details_df = pd.DataFrame(dii_details_data)
            dii_details_df = dii_details_df.reindex(columns=self.column_orders["dii_details"])
            dii_details_df['Shareholder Name'] = dii_details_df['Shareholder Name'].fillna(dii_details_df['Category'])
            dii_details_df.to_csv(output_folder / f"DII_Details_{timestamp}.csv", mode='a', 
                                 header=not (output_folder / f"DII_Details_{timestamp}.csv").exists(), index=False)

        if fii_details_data:
            fii_details_df = pd.DataFrame(fii_details_data)
            fii_details_df = fii_details_df.reindex(columns=self.column_orders["fii_details"])
            fii_details_df['Shareholder Name'] = fii_details_df['Shareholder Name'].fillna(fii_details_df['Category'])
            fii_details_df.to_csv(output_folder / f"FII_Details_{timestamp}.csv", mode='a', 
                                 header=not (output_folder / f"FII_Details_{timestamp}.csv").exists(), index=False)

        self.logger.info(f"Appended data to {output_folder}")

    def process_xbrl_files(self, xbrl_dir, output_dir, file_paths=None, batch_size=1000):
        """Process multiple XBRL files in batches with incremental appending and checkpointing."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_folder = Path(output_dir) / f"output_{timestamp}"
        output_folder.mkdir(parents=True, exist_ok=True)

        # Checkpoint file
        checkpoint_file = output_folder / "processed_checkpoint.txt"
        processed_files = set()
        if checkpoint_file.exists():
            with open(checkpoint_file, "r") as f:
                processed_files = set(line.strip() for line in f)

        # Collect files
        xbrl_dir = Path(xbrl_dir)
        if file_paths is None:
            file_paths = [str(p) for p in xbrl_dir.rglob("*.xml")]
        total_files = len(file_paths)
        remaining_files = [p for p in file_paths if os.path.basename(p) not in processed_files]

        if not remaining_files:
            self.logger.info("All files processed. Exiting.")
            print("All files processed. Exiting.")
            return

        completed_files = 0
        with Pool(processes=6) as pool:
            for i in range(0, len(remaining_files), batch_size):
                batch_paths = remaining_files[i:i + batch_size]
                results = pool.map(self.process_xbrl_file, batch_paths)

                batch_main_data = []
                batch_huf_data = []
                batch_fii_data = []
                batch_dii_data = []
                batch_dii_details_data = []
                batch_fii_details_data = []

                for result in results:
                    if result:
                        main_data, huf_data, fii_data, dii_data, dii_details_data, fii_details_data = result
                        if main_data:
                            batch_main_data.append(main_data)
                        batch_huf_data.extend(huf_data)
                        batch_fii_data.extend(fii_data)
                        batch_dii_data.extend(dii_data)
                        batch_dii_details_data.extend(dii_details_data)
                        batch_fii_details_data.extend(fii_details_data)

                if any([batch_main_data, batch_huf_data, batch_fii_data, batch_dii_data, batch_dii_details_data, batch_fii_details_data]):
                    self.save_batch_data((batch_main_data, batch_huf_data, batch_fii_data, batch_dii_data, batch_dii_details_data, batch_fii_details_data), output_folder, timestamp)

                with open(checkpoint_file, "a") as f:
                    for path in batch_paths:
                        f.write(f"{os.path.basename(path)}\n")
                completed_files += len(batch_paths)
                percentage = (completed_files / total_files) * 100
                sys.stdout.write(f"\rProgress: {percentage:.2f}% ({completed_files}/{total_files})")
                sys.stdout.flush()

                # Clear memory
                batch_main_data.clear()
                batch_huf_data.clear()
                batch_fii_data.clear()
                batch_dii_data.clear()
                batch_dii_details_data.clear()
                batch_fii_details_data.clear()

        print(f"\rProgress: 100.00% ({total_files}/{total_files})")
        self.logger.info(f"Processed {total_files} files. Data in {output_folder}")
        print(f"Processed {total_files} files. Data in {output_folder}")

def main():
    project_root = Path(__file__).resolve().parent.parent.parent
    extractor = ShareholdingNseXbrlExtractor(project_root=project_root)
    xbrl_dir = project_root / "data/shareholding_nse/output/companies_xbrl"
    output_dir = project_root / "data/shareholding_nse/output/shareholding"
    extractor.process_xbrl_files(xbrl_dir, output_dir)

if __name__ == "__main__":
    main()