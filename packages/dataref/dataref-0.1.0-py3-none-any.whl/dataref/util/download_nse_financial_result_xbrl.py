import json
import pandas as pd
import os
import requests
import logging
from datetime import datetime
from pathlib import Path

class FinancialXBRLProcessor:
    def __init__(self, project_root, config_path="config/financial_nse_config.json"):
        self.project_root = Path(project_root).resolve()
        
        # Setup logging
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)

        logging.basicConfig(
            filename=log_dir / "financial_nse_xbrl_extract.log",
            level=logging.INFO,
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

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

    def extract_consolidated_files(self, input_csvs, output_csvs):
        """Extract consolidated rows from each input CSV and save to type-specific outputs."""
        for company_type, input_csv in input_csvs.items():
            output_csv = output_csvs[company_type]
            try:
                input_csv = Path(input_csv)
                output_csv = Path(output_csv)
                output_csv.parent.mkdir(parents=True, exist_ok=True)
                df = pd.read_csv(input_csv)
                logging.info(f"Read {len(df)} rows from {input_csv}")

                # Filter for consolidated files
                col_name = "CONSOLIDATED / NON-CONSOLIDATED"
                consolidated_df = df[df[col_name] == "Consolidated"]
                logging.info(f"Found {len(consolidated_df)} consolidated entries for {company_type}")

                consolidated_df.to_csv(output_csv, index=False)
                logging.info(f"Saved {len(consolidated_df)} rows to {output_csv}")
            except Exception as e:
                logging.error(f"Error processing {input_csv}: {e}")

    def download_xbrl(self, url, file_path):
        """Download XBRL file if it doesn't exist."""
        file_path = Path(file_path)
        if not file_path.exists():
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                response.raise_for_status()
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(response.content)
                logging.info(f"Downloaded XBRL to {file_path}")
                return True
            except Exception as e:
                logging.error(f"Failed to download {url}: {e}")
                return False
        else:
            logging.info(f"XBRL exists at {file_path}, skipping")
            return True

    def download_xbrl_files(self, input_csvs, output_dir):
        """Download XBRL files into type-specific subfolders."""
        output_dir = Path(output_dir)
        for company_type, consolidated_csv in input_csvs.items():
            try:
                consolidated_csv = Path(consolidated_csv)
                df = pd.read_csv(consolidated_csv)
                logging.info(f"Read {len(df)} rows from {consolidated_csv}")

                for _, row in df.iterrows():
                    company = row["COMPANY NAME"]
                    period_ended = row["PERIOD ENDED"]
                    xbrl_url = row["** XBRL"]
                    ind_as_col = "IND AS/ NON IND AS" if company_type in ["equity", "sme"] else "LI / GI" if company_type == "insurance" else None
                    type_value = row[ind_as_col] if ind_as_col in df.columns else ""

                    # Map type to folder
                    if company_type == "equity":
                        type_folder = {"Ind-AS New": "IND-AS", "Non-Ind-AS": "NON-IND-AS", "NBFC-IND": "NBFC-IND"}.get(type_value, "IND-AS")
                    elif company_type == "sme":
                        type_folder = {"Ind-AS New": "IND-AS", "Non-Ind-AS": "NON-IND-AS"}.get(type_value, "IND-AS")
                    elif company_type == "insurance":
                        type_folder = {"Life-Insurance": "LI", "General-Insurance": "GI"}.get(type_value, "LI")
                    else:  # debt
                        type_folder = ""

                    # Determine quarterly or annual
                    period = row["PERIOD"].lower()
                    base_dir = "quarterly" if "quarter" in period else "annually"

                    # Construct path
                    safe_company = company.replace(" ", "_").replace("/", "_").replace("\\", "_")
                    safe_period = period_ended.replace("-", "")
                    company_folder = output_dir / base_dir / company_type.capitalize() / type_folder / safe_company
                    file_path = company_folder / f"{safe_company}_{safe_period}_Consolidated.xml"

                    self.download_xbrl(xbrl_url, file_path)
            except Exception as e:
                logging.error(f"Error processing {consolidated_csv}: {e}")

    def run(self, input_csvs, output_csvs, output_dir):
        self.extract_consolidated_files(input_csvs, output_csvs)
        self.download_xbrl_files(output_csvs, output_dir)

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent.parent
    processor = FinancialXBRLProcessor(project_root=project_root)
    input_csvs = {
        "equity": project_root / "data/financial_nse/input/equity_input.csv",
        "sme": project_root / "data/financial_nse/input/sme_input.csv",
        "debt": project_root / "data/financial_nse/input/debt_input.csv",
        "insurance": project_root / "data/financial_nse/input/insurance_input.csv"
    }
    output_csvs = {
        "equity": project_root / "data/financial_nse/output/consolidated/equity_consolidated.csv",
        "sme": project_root / "data/financial_nse/output/consolidated/sme_consolidated.csv",
        "debt": project_root / "data/financial_nse/output/consolidated/debt_consolidated.csv",
        "insurance": project_root / "data/financial_nse/output/consolidated/insurance_consolidated.csv"
    }
    output_dir = project_root / "data/financial_nse/input/fundamental_data"
    processor.run(input_csvs, output_csvs, output_dir)