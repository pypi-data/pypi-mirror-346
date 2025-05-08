import os
import time
import requests
import pandas as pd

from pathlib import Path
from datetime import datetime, timedelta

from openrte.tools import Logger

class Retriever:
    def __init__(self, token: str, logger: Logger):
        self.token = token
        self.logger = logger
        self.request_base_url = "https://digital.iservices.rte-france.com/open_api"

        self.headers = {
            "User-Agent": "rte-api-wrapper (contact: henriupton99@gmail.com)",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _get_request_url_from_key(self, key: str) -> str:
        mapping = {
            "actual_generations_per_production_type": f"{self.request_base_url}/actual_generation/v1/actual_generations_per_production_type",
            "actual_generations_per_unit": f"{self.request_base_url}/actual_generation/v1/actual_generations_per_unit"
        }
        if key not in mapping:
            raise KeyError(f"Invalid input 'data_type' keyword: '{key}'. Must be one of {list(mapping.keys())}")
        return mapping[key]
    
    @staticmethod
    def _convert_date_to_iso8601(date: datetime) -> datetime:
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def _convert_date_to_datetime(date_str: str) -> datetime:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return date
        except ValueError:
            raise ValueError("Invalid date format. Expected 'YYYY-MM-DD HH:MM:SS'")
    
    def _generate_tasks(self, start_date: str, end_date: str, base_url: str) -> list[str]:
        task_start_date = start_date
        tasks = []
        while task_start_date < end_date:
            task_end_date = min(task_start_date + timedelta(days=7), end_date)
            start = self._convert_date_to_iso8601(task_start_date)
            end = self._convert_date_to_iso8601(task_end_date)
            tasks.append(f"{base_url}?start_date={start}&end_date={end}")
            task_start_date = task_end_date
        return tasks
    
    @staticmethod
    def _convert_json_to_dataframe(data, dtype):
        metas = {
            "actual_generations_per_production_type": ["production_type"],
            "actual_generations_per_unit": [['unit', 'eic_code'], ['unit', 'name'], ['unit', 'production_type']]
            }
        df = pd.json_normalize(data[dtype], meta=metas[dtype], record_path=["values"], sep="_")
        return df

    def retrieve(self, start_date: str, end_date: str, data_type: list[str] | str, output_dir: str | None = None) -> dict:
        
        if output_dir is not None:
          output_dir = Path(output_dir)
          if not output_dir.exists():
              os.makedirs(output_dir, exist_ok=True)

        if isinstance(data_type, str):
            data_type = data_type.split(",")

        start_date = self._convert_date_to_datetime(start_date)
        end_date = self._convert_date_to_datetime(end_date)

        if (end_date - start_date).days < 1:
            raise ValueError("Retrieval error : Time difference between input end_date and start_date must be greather than 1 day")
        
        dfs = {}

        for dtype in data_type:
            base_url = self._get_request_url_from_key(dtype)
            tasks = self._generate_tasks(start_date, end_date, base_url)
            df_final = pd.DataFrame()

            for url in tasks:
              self.logger.info(f"Requesting '{dtype}' from URL: {url}")

              start_time = time.time()
              response = requests.get(url, headers=self.headers)

              if response.status_code == 200:
                  elapsed = round(time.time() - start_time, 4)
                  self.logger.info(f"Success: '{dtype}' retrieved in {elapsed} seconds")
                  data = response.json()
                  df = self._convert_json_to_dataframe(data, dtype)
                  df_final = pd.concat([df_final, df])
              else:
                  self.logger.error(f"Failed to retrieve '{dtype}': {response.status_code} - {response.text}")
              
              if output_dir is not None:
                start = start_date.strftime("%Y%m%d")
                end = end_date.strftime("%Y%m%d")
                filepath = os.path.join(output_dir, f"{dtype}_{start}-{end}.csv")
                df_final.to_csv(filepath, sep=",", index=False)
                self.logger.info(f"Data saved at path : {filepath}")

              time.sleep(2)

            dfs[dtype] = df_final

        return dfs
