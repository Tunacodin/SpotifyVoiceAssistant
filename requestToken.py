import requests
from base64 import b64encode
import webbrowser

# Spotify Kimlik Bilgileri
client_id = "dc01cdb42426482493043b7ada5e3ab5"
client_secret = "b27021594092487c87379e1aff34c267"
redirect_uri = "http://localhost:8888/callback"
scope = "user-modify-playback-state user-read-playback-state"

# Authorization URL oluştur
auth_url = (
    f"https://accounts.spotify.com/authorize?"
    f"client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
)
webbrowser.open(auth_url)

# Kullanıcıdan Authorization Code al
auth_code = input("Authorization Code'u buraya yapıştırın: ")

# Access Token almak için istek gönder
auth_header = b64encode(f"{client_id}:{client_secret}".encode()).decode()
url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": f"Basic {auth_header}",
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": redirect_uri
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    tokens = response.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
else:
    print("Hata:", response.status_code, response.text)
