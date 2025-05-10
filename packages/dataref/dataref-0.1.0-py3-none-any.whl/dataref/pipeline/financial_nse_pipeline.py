import json
import pandas as pd
import os
import logging
from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path

class FinancialNSEPipeline:
    def __init__(self, project_root, config_path="config/financial_nse_config.json"):
        self.project_root = Path(project_root).resolve()
        
        # Ensure the logs directory exists
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)

        # Setup logging
        log_file = log_dir / "financial_nse_xbrl_extract.log"
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        # Load configuration
        config_path = self.project_root / config_path
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            logging.error(f"Config file not found at {config_path}")
            raise

        self.xbrl_tags = self.config["xbrl_tags"]

        # Define column orders for each type and subtype
        self.column_orders = {}
        for company_type in self.xbrl_tags:
            self.column_orders[company_type] = {}
            for subtype in self.xbrl_tags[company_type]:
                fixed_columns = ["Date", "CompanyName"]
                config_columns = []
                for category in self.xbrl_tags[company_type][subtype]:
                    if category != "metadata":
                        for field in self.xbrl_tags[company_type][subtype][category]:
                            if field != "contextRef" and field not in config_columns:
                                config_columns.append(field)
                metadata_columns = [field for field in self.xbrl_tags[company_type][subtype]["metadata"] if field != "contextRef"]
                additional_columns = ["Subtype"]
                self.column_orders[company_type][subtype] = fixed_columns + metadata_columns + config_columns + additional_columns

    def parse_xbrl(self, file_path, tags):
        """Parse XBRL file using BeautifulSoup with the provided tag block."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "lxml-xml")

            extracted_data = {}
            end_date = None
            cash_balance_count = 0

            for category, fields in tags.items():
                priority_contexts = fields.get("contextRef", [])
                logging.debug(f"Processing category {category} with contextRefs: {priority_contexts}")
                for field_name, tag_list in fields.items():
                    if field_name == "contextRef":
                        continue

                    value = None
                    found_context = None
                    for tag in tag_list:
                        for prefix in ["", "in-bse-fin:", "ind-as:", "xbrli:", "ifrs-full:", "nbfc-ind:", "in-capmkt:"]:
                            full_tag = prefix + tag
                            elements = soup.find_all(full_tag)
                            logging.debug(f"Searching for tag: {full_tag}, found {len(elements)} elements")
                            for element in elements:
                                if element.has_attr("contextRef"):
                                    context_ref = element["contextRef"]
                                    logging.debug(f"Found element with contextRef={context_ref}: {element.text.strip()}")
                                    if tag == "CashAndCashEquivalentsCashFlowStatement":
                                        cash_balance_count += 1
                                        if field_name == "Opening Balance of CashAndCashEquivalents" and cash_balance_count == 1:
                                            if context_ref in priority_contexts:
                                                value = element.text.strip()
                                                found_context = context_ref
                                                break
                                        elif field_name == "Closing Balance of CashAndCashEquivalents" and cash_balance_count == 2:
                                            if context_ref in priority_contexts:
                                                value = element.text.strip()
                                                found_context = context_ref
                                                break
                                    elif context_ref in priority_contexts:
                                        value = element.text.strip()
                                        found_context = context_ref
                                        break
                            if value:
                                break
                        if value:
                            break

                    if value:
                        try:
                            if field_name not in ["CompanyIdentifier", "CompanyName", "MSEISymbol", "ISIN", "ClassOfSecurity", "TypeOfInsurance"]:
                                extracted_data[field_name] = float(value)
                            else:
                                extracted_data[field_name] = value
                            logging.info(f"Extracted {field_name}: {value} (contextRef={found_context})")
                        except ValueError:
                            extracted_data[field_name] = value
                            logging.info(f"Extracted {field_name}: {value} (contextRef={found_context}, non-numeric)")
                    else:
                        logging.debug(f"No value found for {field_name} in {file_path}")

            metadata_contexts = tags.get("metadata", {}).get("contextRef", [])
            for context in soup.find_all("xbrli:context"):
                if context.get("id") in metadata_contexts:
                    period = context.find("xbrli:endDate") or context.find("xbrli:instant")
                    if period and period.text:
                        try:
                            end_date = datetime.strptime(period.text, "%Y-%m-%d").date()
                            logging.info(f"Extracted end_date: {end_date}")
                        except ValueError:
                            logging.warning(f"Invalid date format in {file_path}: {period.text}")
                        break

            logging.info(f"Parsed {file_path} successfully")
            return extracted_data, end_date
        except Exception as e:
            logging.error(f"Error parsing {file_path}: {e}")
            return None, None

    def get_subtype_from_path(self, file_path, company_type):
        """Extract the subtype from the file path."""
        file_path = Path(file_path)
        parts = file_path.parts
        try:
            subtype_index = parts.index(company_type.capitalize()) + 1
            subtype = parts[subtype_index]
            valid_subtypes = self.xbrl_tags[company_type].keys()
            if subtype not in valid_subtypes:
                logging.warning(f"Invalid subtype {subtype} in {file_path}, defaulting to first subtype")
                return list(valid_subtypes)[0]
            return subtype
        except (ValueError, IndexError):
            logging.error(f"Could not determine subtype from {file_path}, defaulting to first subtype")
            return list(valid_subtypes)[0]

    def get_versioned_output_dir(self, base_dir):
        """Generate a versioned output directory with a timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        versioned_dir = Path(base_dir) / f"output_{timestamp}"
        versioned_dir.mkdir(parents=True, exist_ok=True)
        return versioned_dir

    def parse_xbrl_files(self, xbrl_dir, output_dir):
        """Parse XBRL files and output to subtype-specific CSVs in a versioned folder."""
        xbrl_dir = Path(xbrl_dir)
        output_dir = Path(output_dir)
        data_by_type = {
            "equity": {"IND-AS": [], "NON-IND-AS": [], "NBFC-IND": []},
            "sme": {"IND-AS": [], "NON-IND-AS": []},
            "debt": {"DEBT": []},
            "insurance": {"GI": [], "LI": []}
        }

        for period_dir in ["quarterly", "annually"]:
            period_path = xbrl_dir / period_dir
            if not period_path.exists():
                logging.warning(f"Directory not found: {period_path}")
                continue

            for company_type in data_by_type:
                type_path = period_path / company_type.capitalize()
                if not type_path.exists():
                    logging.warning(f"Directory not found: {type_path}")
                    continue

                for sub_type in type_path.iterdir():
                    sub_path = sub_type
                    if not sub_path.is_dir():
                        continue
                    for company_folder in sub_path.iterdir():
                        company_path = company_folder
                        if not company_path.is_dir():
                            continue
                        for file_name in company_path.iterdir():
                            if str(file_name).endswith("_Consolidated.xml"):
                                file_path = file_name
                                logging.info(f"Processing file: {file_path}")
                                parts = file_name.name.split("_")
                                try:
                                    company_name = "_".join(parts[:-2]).replace("_", " ")
                                    period_ended = parts[-2][:2] + "-" + parts[-2][2:5] + "-" + parts[-2][5:]
                                except IndexError:
                                    logging.error(f"Invalid filename format: {file_name}")
                                    continue

                                subtype = self.get_subtype_from_path(file_path, company_type)
                                tags = self.xbrl_tags[company_type][subtype]

                                extracted_data, xbrl_date = self.parse_xbrl(file_path, tags)
                                if extracted_data:
                                    row_data = {
                                        "Date": xbrl_date.strftime("%Y-%m-%d") if xbrl_date else period_ended,
                                        **extracted_data,
                                        "CompanyName": company_name,
                                        "Subtype": subtype
                                    }
                                    data_by_type[company_type][subtype].append(row_data)
                                else:
                                    logging.warning(f"No data extracted from {file_path}")

        # Create a versioned output directory
        versioned_output_dir = self.get_versioned_output_dir(output_dir)

        # Save data to CSVs in the versioned directory
        for company_type, subtypes_data in data_by_type.items():
            output_base = self.config["paths"]["fundamentals"][company_type]
            if isinstance(output_base, dict):
                for subtype, data_list in subtypes_data.items():
                    if data_list:
                        df = pd.DataFrame(data_list)
                        base_path = output_base[subtype]
                        filename = Path(base_path).name
                        output_path = versioned_output_dir / filename
                        df = df.reindex(columns=self.column_orders[company_type][subtype])
                        df.to_csv(output_path, index=False)
                        logging.info(f"Saved {len(df)} rows to {output_path}")
                    else:
                        logging.warning(f"No data to save for {company_type}/{subtype}")
            else:
                all_data = []
                for subtype, data_list in subtypes_data.items():
                    all_data.extend(data_list)
                if all_data:
                    df = pd.DataFrame(all_data)
                    filename = Path(output_base).name
                    output_path = versioned_output_dir / filename
                    first_subtype = list(self.xbrl_tags[company_type].keys())[0]
                    df = df.reindex(columns=self.column_orders[company_type][first_subtype])
                    df.to_csv(output_path, index=False)
                    logging.info(f"Saved {len(df)} rows to {output_path}")
                else:
                    logging.warning(f"No data to save for {company_type}")

    def run(self, xbrl_dir, output_dir):
        self.parse_xbrl_files(xbrl_dir, output_dir)

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent.parent
    pipeline = FinancialNSEPipeline(project_root=project_root)
    xbrl_dir = project_root / "data/financial_nse/input/fundamental_data"
    output_dir = project_root / "data/financial_nse/output/fundamentals"
    pipeline.run(xbrl_dir, output_dir)