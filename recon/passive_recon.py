# passive_recon.py
# by @rootnorth (github)

import requests
import json
import time

class PassiveReconScanner:
    def __init__(self, domain):
        self.domain = domain
        self.subdomains = set()

    def crtsh_query(self):
        """crt.sh üzerinden alt domain sorgulama"""
        url = f"https://crt.sh/?q=%25.{self.domain}&output=json"
        try:
            print("[*] crt.sh sorgusu başlatılıyor...")
            resp = requests.get(url, timeout=15)
            if resp.status_code != 200:
                print(f"crt.sh API hatası: HTTP {resp.status_code}")
                return
            data = resp.json()
            for entry in data:
                names = entry.get('name_value', '')
                for sub in names.split('\n'):
                    sub = sub.strip()
                    if sub.endswith(self.domain):
                        self.subdomains.add(sub.lower())
            print(f"[+] crt.sh'dan {len(self.subdomains)} alt domain bulundu.")
        except Exception as e:
            print(f"crt.sh sorgu hatası: {e}")

    def securitytrails_query(self, api_key):
        """SecurityTrails API ile alt domain sorgulama (API anahtarı gerekir)"""
        url = f"https://api.securitytrails.com/v1/domain/{self.domain}/subdomains"
        headers = {"APIKEY": api_key}
        try:
            print("[*] SecurityTrails API sorgusu başlatılıyor...")
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code != 200:
                print(f"SecurityTrails API hatası: HTTP {resp.status_code}")
                return
            data = resp.json()
            subs = data.get('subdomains', [])
            for sub in subs:
                full_sub = f"{sub}.{self.domain}"
                self.subdomains.add(full_sub.lower())
            print(f"[+] SecurityTrails'dan {len(subs)} alt domain eklendi.")
        except Exception as e:
            print(f"SecurityTrails sorgu hatası: {e}")

    def run(self):
        print(f"=== Passive Recon Scanner - {self.domain} ===")
        self.crtsh_query()

        # Eğer API anahtarın varsa aç, yoksa pas geç
        api_key = input("SecurityTrails API key (yoksa boş bırak): ").strip()
        if api_key:
            self.securitytrails_query(api_key)

        print(f"\nToplam bulunan alt domain sayısı: {len(self.subdomains)}")
        for sub in sorted(self.subdomains):
            print(f" - {sub}")

if __name__ == "__main__":
    domain = input("Hedef domain girin: ").strip()
    scanner = PassiveReconScanner(domain)
    scanner.run()
