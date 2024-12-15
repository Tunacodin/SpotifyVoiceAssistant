import requests
import speech_recognition as sr
from base64 import b64encode
import os

# Spotify API Bilgileri
CLIENT_ID = "dc01cdb42426482493043b7ada5e3ab5"
CLIENT_SECRET = "b27021594092487c87379e1aff34c267"
REDIRECT_URI = "http://localhost:8888/callback"
REFRESH_TOKEN_FILE = "refresh_token.txt"

# Refresh Token'ı dosyaya kaydetme ve okuma
def save_refresh_token(token):
    with open(REFRESH_TOKEN_FILE, "w") as file:
        file.write(token)

def load_refresh_token():
    if os.path.exists(REFRESH_TOKEN_FILE):
        with open(REFRESH_TOKEN_FILE, "r") as file:
            return file.read().strip()
    return None

# Access Token alma veya yenileme
def get_access_token(auth_code=None):
    refresh_token = load_refresh_token()
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    if auth_code:
        data = {"grant_type": "authorization_code", "code": auth_code, "redirect_uri": REDIRECT_URI}
    elif refresh_token:
        data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    else:
        print("Authorization Code veya Refresh Token mevcut değil.")
        return None

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens.get("access_token")
        new_refresh_token = tokens.get("refresh_token")

        # Yeni Refresh Token varsa kaydet
        if new_refresh_token:
            save_refresh_token(new_refresh_token)

        return access_token
    else:
        print(f"Token alınamadı: {response.status_code}, {response.text}")
        return None

# Sesli komut alma
def listen_to_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Lütfen bir komut söyleyin:")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio, language="tr-TR")
            print(f"Algılanan Komut: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Ses anlaşılamadı. Lütfen tekrar deneyin.")
            return None
        except sr.RequestError as e:
            print(f"API Hatası: {e}")
            return None

# Şarkıyı çalma
def play_song(track_uri, access_token):
    url = "https://api.spotify.com/v1/me/player/play"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    data = {"uris": [track_uri]}

    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 204:
        print("Şarkı çalınıyor!")
    else:
        print(f"Şarkı çalma hatası: {response.status_code}, {response.text}")

# Şarkıyı durdurma
def pause_song(access_token):
    url = "https://api.spotify.com/v1/me/player/pause"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.put(url, headers=headers)
    if response.status_code == 204:
        print("Şarkı durduruldu.")
    else:
        print(f"Şarkıyı durdurma hatası: {response.status_code}, {response.text}")

# Şarkıyı devam ettirme
def resume_song(access_token):
    url = "https://api.spotify.com/v1/me/player/play"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.put(url, headers=headers)
    if response.status_code == 204:
        print("Şarkı devam ettiriliyor!")
    else:
        print(f"Şarkıyı devam ettirme hatası: {response.status_code}, {response.text}")

# Sıradaki şarkıya geçme
def next_song(access_token):
    url = "https://api.spotify.com/v1/me/player/next"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.post(url, headers=headers)
    if response.status_code == 204:
        print("Sıradaki şarkıya geçildi.")
    else:
        print(f"Sıradaki şarkıya geçerken hata: {response.status_code}, {response.text}")

# Önceki şarkıya dönme
def previous_song(access_token):
    url = "https://api.spotify.com/v1/me/player/previous"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.post(url, headers=headers)
    if response.status_code == 204:
        print("Önceki şarkıya dönüldü.")
    else:
        print(f"Önceki şarkıya dönerken hata: {response.status_code}, {response.text}")

# Şarkı arama
def search_song(query, access_token):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": query, "type": "track", "limit": 1}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        tracks = response.json().get("tracks", {}).get("items", [])
        if tracks:
            track_uri = tracks[0]["uri"]
            print(f"Bulunan Şarkı: {tracks[0]['name']} - {tracks[0]['artists'][0]['name']}")
            print(f"Spotify URI: {track_uri}")
            return track_uri
    print(f"Şarkı arama hatası: {response.status_code}, {response.text}")
    return None

# Komut işleme
def process_command(command, access_token):
    if "çal" in command:
        query = command.replace("çal", "").strip()
        if query:
            track_uri = search_song(query, access_token)
            if track_uri:
                play_song(track_uri, access_token)
                return True
            else:
                print("Şarkı bulunamadı.")
                return True
    elif "şarkıyı durdur" in command:
        pause_song(access_token)
        return True
    elif "devam ettir" in command:
        resume_song(access_token)
        return True
    elif "sonraki" in command:
        next_song(access_token)
        return True
    elif "önceki" in command:
        previous_song(access_token)
        return True
    elif "spotify'ı kapat" in command:
        print("Spotify Asistanı kapatılıyor.")
        return False
    else:
        print("Geçerli bir komut algılanamadı. Lütfen tekrar deneyin.")
        return True

# Ana akış
def main():
    print("Spotify Sesli Komut Asistanı Başlatılıyor...")
    access_token = get_access_token()
    if not access_token:
        print("Yetkilendirme gerekiyor. Authorization Code alın.")
        return

    while True:
        command = listen_to_command()
        if command:
            keep_running = process_command(command, access_token)
            if not keep_running:
                break

if __name__ == "__main__":
    main()
