import requests
from base64 import b64encode
import webbrowser

# Spotify API Bilgileri
CLIENT_ID = "af1bde8bd74c407aa0acdfaf7534d6a3"
CLIENT_SECRET = "1a40545de2624fd7aca585e1c182a388"
REDIRECT_URI = "http://localhost:8888/callback"
REFRESH_TOKEN = "AQBqBewvBEHGRgNdmMsjsGpQnvgXUxU8VNnPJt8zL6gCq07j2qU6ap06xSYpoo9TNBGNmnR-t4p_Wah8m4H64nBvJ0hPG5baIowj4KLk-ShH_MSEuR8rwYOU-MoC5NWdbtY"

# Spotify API Yetkilendirme İçin Gerekli Scope'lar
SCOPES = "user-modify-playback-state user-read-playback-state"

def generate_authorization_url():
    """
    Kullanıcıyı yetkilendirme ekranına yönlendiren URL'yi oluşturur.
    """
    url = (
        f"https://accounts.spotify.com/authorize"
        f"?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES}"
    )
    print(f"Yetkilendirme URL'si: {url}")
    webbrowser.open(url)

def get_access_token(auth_code):
    """
    Authorization Code kullanarak Access Token ve Refresh Token alır.
    """
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        tokens = response.json()
        print("Access Token:", tokens.get("access_token"))
        print("Refresh Token:", tokens.get("refresh_token"))
        return tokens.get("access_token"), tokens.get("refresh_token")
    else:
        print(f"Access Token alınamadı: {response.status_code}, {response.text}")
        return None, None

def refresh_access_token():
    """
    Refresh Token kullanarak yeni bir Access Token alır.
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
        new_access_token = response.json().get("access_token")
        print("Yeni Access Token:", new_access_token)
        return new_access_token
    else:
        print(f"Access Token yenilenemedi: {response.status_code}, {response.text}")
        return None

def check_access_token(access_token):
    """
    Access Token'in geçerli olup olmadığını ve scope'ları kontrol eder.
    """
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Access Token geçerli.")
        print("Scope'lar doğru şekilde tanımlanmıştır.")
        return True
    else:
        print(f"Access Token geçerli değil: {response.status_code}, {response.text}")
        return False

def main():
    print("Spotify Scope İşlemleri Başlatılıyor...")

    # Yetkilendirme URL'sini oluştur ve kullanıcıyı yönlendir
    print("Kullanıcıdan Authorization Code alınacak...")
    generate_authorization_url()

    # Kullanıcıdan Authorization Code alın
    auth_code = input("Authorization Code'unuzu girin: ")

    # Access Token ve Refresh Token al
    access_token, refresh_token = get_access_token(auth_code)
    if not access_token:
        print("Access Token alınamadı. Program sonlandırılıyor.")
        return

    # Access Token doğrula
    if not check_access_token(access_token):
        print("Access Token geçersiz. Program sonlandırılıyor.")
        return

    # Refresh Token ile yeni Access Token al
    print("Access Token yenileniyor...")
    new_access_token = refresh_access_token()
    if new_access_token:
        print("Yeni Access Token alındı. İşlem tamamlandı.")

if __name__ == "__main__":
    main()
