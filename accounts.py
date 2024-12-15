import requests

def get_active_devices(access_token):
    """
    Spotify'da aktif cihazları listeler.
    """
    url = "https://api.spotify.com/v1/me/player/devices"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    print(f"API Yanıt Kodu: {response.status_code}")
    if response.status_code == 200:
        devices = response.json().get("devices", [])
        if not devices:
            print("Spotify'da aktif cihaz bulunamadı.")
        else:
            for device in devices:
                print(f"Cihaz Adı: {device['name']}, Durum: {'Aktif' if device['is_active'] else 'Pasif'}")
    elif response.status_code == 401:
        print("Hata: Access Token geçersiz veya eksik. Lütfen geçerli bir Access Token ekleyin.")
    else:
        print(f"API Yanıtı: {response.text}")
