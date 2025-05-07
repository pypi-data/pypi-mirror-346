
import os
import requests
from dotenv import load_dotenv

class client:
    def __init__(self, base_url="https://api.andromeda.prosilico.com/api/v1.0"):
        load_dotenv()
        self.base_url = os.getenv("INFERENCE_URL", base_url)
        self.token = os.getenv("INFERENCE_API_TOKEN")

        if not self.token:
            raise ValueError("Token not found in .env file (INFERENCE_API_TOKEN)")

    def predict(self, molecule: str):
        url = f"{self.base_url}/predict/"
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }

        payload = {"molecule": molecule}

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()