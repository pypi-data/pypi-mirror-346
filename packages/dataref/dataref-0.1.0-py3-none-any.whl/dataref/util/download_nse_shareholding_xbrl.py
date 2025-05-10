import csv
import os
import requests
import logging
from datetime import datetime
from multiprocessing import Pool
from functools import partial
from pathlib import Path
import sys
import json

class ShareholdingNSEDownloader:
    def __init__(self, project_root, config_path="config/shareholding_nse_config.json"):
        """Initialize downloader with project root and setup logging."""
        self.project_root = Path(project_root).resolve()
        self.log_dir = self.project_root / "logs"
        self.log_dir.mkdir(exist_ok=True)

        # Configure logging
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.handlers = []  # Clear existing handlers
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

        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

    def download_file(self, args):
        """Download a single XBRL file into a company-specific folder if it doesn't already exist."""
        url, company, output_dir = args
        company_folder = output_dir / company
        company_folder.mkdir(parents=True, exist_ok=True)
        filename = company_folder / (os.path.basename(url) if url.endswith('.xml') else 'file.xml')

        # Check if file already exists
        if filename.exists():
            self.logger.info(f"XBRL exists at {filename}, skipping")
            return True, str(filename)

        # Proceed with download
        try:
            response = requests.get(url, headers=self.HEADERS, timeout=10, stream=True)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            self.logger.info(f"Downloaded XBRL to {filename} from {url}")
            return True, str(filename)
        except requests.RequestException as e:
            self.logger.error(f"Failed to download {url} for {company}: {e}")
            return False, str(filename)

    def download_xbrl_files(self, input_csv_path, output_dir, max_workers=10, batch_size=100):
        """Download XBRL files from URLs in the input CSV with parallel processing."""
        input_csv_path = Path(input_csv_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Count total files from CSV
        try:
            with open(input_csv_path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                total_files = sum(1 for _ in reader)
        except FileNotFoundError:
            self.logger.error(f"Input CSV not found at {input_csv_path}")
            raise
        if total_files == 0:
            self.logger.warning(f"No URLs found in {input_csv_path}")
            print("No URLs found in input CSV. Exiting.")
            return

        # Read download tasks
        with open(input_csv_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            download_tasks = [(row["ACTION"], row["COMPANY"].replace(" ", "_").replace("&", "and"), output_dir) for row in reader]

        completed_files = 0
        with Pool(processes=max_workers) as pool:
            for i in range(0, len(download_tasks), batch_size):
                batch_tasks = download_tasks[i:i + batch_size]
                results = pool.map(self.download_file, batch_tasks)

                # Update progress
                batch_completed = sum(1 for success, _ in results if success)
                completed_files += batch_completed
                percentage = (completed_files / total_files) * 100
                sys.stdout.write(f"\rProgress: {percentage:.2f}% ({completed_files}/{total_files})")
                sys.stdout.flush()

        print(f"\rProgress: 100.00% ({total_files}/{total_files})")
        self.logger.info(f"Completed downloading {total_files} XBRL files to {output_dir}")
        failed_count = total_files - completed_files
        if failed_count > 0:
            self.logger.warning(f"{failed_count} files failed to download")
            print(f"Warning: {failed_count} files failed to download. Check logs for details.")

    def run_download(self, input_csv_path, output_dir):
        """Run the shareholding NSE XBRL download process."""
        input_csv_path = Path(input_csv_path)
        output_dir = Path(output_dir)
        if not input_csv_path.exists():
            self.logger.error(f"Input CSV not found at {input_csv_path}")
            print(f"Input CSV not found at {input_csv_path}. Exiting.")
            return
        self.download_xbrl_files(input_csv_path, output_dir, max_workers=10, batch_size=100)
        self.logger.info("XBRL download process completed")

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent.parent
    downloader = ShareholdingNSEDownloader(project_root=project_root)
    input_csv_path = project_root / "data/shareholding_nse/input/equity_input.csv"
    output_dir = project_root / "data/shareholding_nse/output/companies_xbrl"
    downloader.run_download(input_csv_path, output_dir)