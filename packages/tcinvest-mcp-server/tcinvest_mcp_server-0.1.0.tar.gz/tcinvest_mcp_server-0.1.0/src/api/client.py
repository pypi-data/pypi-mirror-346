import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class ApiClient:
    def __init__(self, auth_key: str, base_url: str):
        logger.info("Initializing ApiClient, base_url: %s", base_url)
        self.auth_key = auth_key
        self.base_url = base_url
        self.headers = {}
        self.headers = {
            "sec-ch-ua-platform": "Windows",
            "Authorization": f"Bearer {self.auth_key}",
            "Referer": "https://tcinvest.tcbs.com.vn/",
            "Accept-language": "vi",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def get(self, endpoint: str, params: dict = None):
        logger.info(f"GET request to {self.base_url}/{endpoint} with params: {params}")
        response = requests.get(f"{self.base_url}/{endpoint}", headers=self.headers, params=params)
        if response.status_code == 200:
            logger.info(f"GET request successful, response: {response.json()}")
            return response.json()
        else:
            logger.error(f"GET request failed with status code: {response.status_code}, response: {response.text}") 
            response.raise_for_status()

    def post(self, endpoint: str, data: dict = None):
        logger.info(f"POST request to {self.base_url}/{endpoint} with data: {data}")
        response = requests.post(f"{self.base_url}/{endpoint}", headers=self.headers, json=data)
        if response.status_code == 200:
            logger.info(f"POST request successful, response: {response.json()}")
            return response.json()
        else:
            logger.error(f"POST request failed with status code: {response.status_code}, response: {response.text}")
            response.raise_for_status()