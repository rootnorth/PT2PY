# deepwebbreachscan.py
# by @rootnorth (github)

import requests

class BreachScanner:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "User-Agent": "PT2PY Tool by @rootnorth",
            "hibp-api-key": self.api_key,
            "Accept": "application/json"
        }
        self.api_url = "https://haveibeenpwned.com/api/v3/breachedaccount/"

    def check_breach(self, email):
        url = self.api_url + email
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                breaches = response.json()
                print(f"[!] {email} için veri sızıntısı bulundu:")
                for breach in breaches:
                    print(f" - {breach['Title']} ({breach['BreachDate']})")
            elif response.status_code == 404:
                print(f"[+] {email} için herhangi bir sızıntı bulunamadı.")
            elif response.status_code == 401:
                print("[!] API anahtarınız geçersiz veya yetkisiz.")
            else:
                print(f"[!] Hata oluştu: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[!] İstek sırasında hata oluştu: {e}")

def run():
    print("=== Dark Web & Breach Data Scanner ===")
    api_key = input("HaveIBeenPwned API anahtarınızı girin (https://haveibeenpwned.com/API): ").strip()
    if not api_key:
        print("API anahtarı gerekli!")
        return
    email = input("Kontrol edilecek e-posta adresini girin: ").strip()
    scanner = BreachScanner(api_key)
    scanner.check_breach(email)

if __name__ == "__main__":
    run()
