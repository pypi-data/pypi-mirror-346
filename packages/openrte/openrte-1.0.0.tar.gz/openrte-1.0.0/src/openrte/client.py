import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth

from openrte.tools import Logger
from openrte.retriever import Retriever

class Client:
  credentials = ["client_id", "client_secret"]
  token_url = "https://digital.iservices.rte-france.com/token/oauth/"
  request_base_url = "https://digital.iservices.rte-france.com/open_api"
  
  def _get_access_token(self):
    self.logger.info("Generate access token")
    data = {"grant_type": "client_credentials"}
    auth = HTTPBasicAuth(self.client_id, self.client_secret)
    response = requests.post(self.token_url, data=data, auth=auth)

    if response.status_code == 200:
        self.logger.info("Access token generated successfully")
        return response.json()["access_token"]
    else:
        raise Exception(f"Access token error : {response.status_code} - {response.text}")
    
  def _get_request_url_from_key(self, key: str):
    mapping = {
        "production_per_type": f"{self.request_base_url}/actual_generation/v1/actual_generations_per_production_type",
        "production_per_unit": f"{self.request_base_url}/actual_generation/v1/actual_generations_per_production_unit"
      }
    if key not in mapping:
       raise KeyError(f"Invalid input 'data_type' keyword : '{key}'. Key must be in {mapping.keys()}")
    return mapping[key]
  
  @staticmethod
  def _convert_date_to_iso8601(date_str: str):
    try:
      date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
      return date.strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise ValueError("Invalid date format. Desired format is 'YYYY-MM-DD HH:MM:SS'")
  
  def retrieve_data(self, start_date: str, end_date: str, data_type: list[str] | str, output_dir: str | None = None):
    if output_dir is None:
      return self.retriever.retrieve(start_date, end_date, data_type)
    else:
      return self.retriever.retrieve(start_date, end_date, data_type, output_dir)

  def __init__(self, client_id: str, client_secret: str):
    self.logger = Logger().logger

    self.client_id = client_id
    self.client_secret = client_secret
    
    self.token = self._get_access_token()
    self.retriever = Retriever(token=self.token, logger=self.logger)


