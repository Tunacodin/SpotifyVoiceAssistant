import requests
from base64 import b64encode
from config.settings import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN

def get_access_token_with_refresh():
    """
    Refresh Token kullanarak Access Token alır.
    """
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Access Token alınamadı: {response.status_code}, {response.text}")
        return None
