import requests
from .config import BASE_URL

class Auth:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_login_token(self):
        login_url = f"{BASE_URL}/api/login-api-key"

        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(login_url, headers=headers, timeout=40)
            response.raise_for_status()
            return response.json().get("token"), "Login successful"
        except requests.RequestException as ex:
            if response.content:
                print(response.content)
            return None, "Login failed"