import os
import socket
import subprocess
import http.client
from datetime import datetime

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print("""
░▒▓███████▓▒░▒▓████████▓▒░▒▓███████▓▒░░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░          ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░          ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓███████▓▒░  ░▒▓█▓▒░    ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░  
░▒▓█▓▒░        ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░         ░▒▓█▓▒░     
░▒▓█▓▒░        ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░         ░▒▓█▓▒░     
░▒▓█▓▒░        ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓█▓▒░         ░▒▓█▓▒░ 
             RECON TOOLKIT | PT2PY

    """)

def ping_target(target):
    print(f"\n[*] {target} için ping atılıyor...\n")
    result = os.system(f"ping -c 4 {target}" if os.name != "nt" else f"ping {target}")
    if result != 0:
        print("[!] Ping başarısız.")

def dns_lookup(target):
    print(f"\n[*] {target} için DNS çözümleme...\n")
    try:
        ip = socket.gethostbyname(target)
        host = socket.gethostbyaddr(ip)[0]
        print(f"IP: {ip}")
        print(f"Hostname: {host}")
    except socket.gaierror:
        print("[!] DNS çözümleme başarısız.")

def port_scan(target):
    print(f"\n[*] {target} için port taraması (1-1024)...\n")
    try:
        ip = socket.gethostbyname(target)
        for port in range(1, 1025):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f"[+] Açık Port: {port}")
            sock.close()
    except Exception as e:
        print(f"[!] Hata: {e}")

def basic_whois(ip):
    print(f"\n[*] {ip} için WHOIS benzeri bilgi...\n")
    try:
        print(f"Tarih: {datetime.now()}")
        print(f"IP Adresi: {ip}")
        print(f"Hostname: {socket.getfqdn(ip)}")
    except:
        print("[!] IP bilgisi alınamadı.")

def http_headers(target):
    print(f"\n[*] {target} için HTTP başlıkları alınıyor...\n")
    try:
        conn = http.client.HTTPConnection(target, timeout=5)
        conn.request("HEAD", "/")
        res = conn.getresponse()
        for header in res.getheaders():
            print(f"{header[0]}: {header[1]}")
        conn.close()
    except Exception as e:
        print(f"[!] Hata: {e}")

def main():
    while True:
        clear()
        banner()
        print("""
[1] Ping At
[2] DNS Çözümle
[3] Port Taraması
[4] Basit IP Whois
[5] HTTP Başlıklarını Al
[0] Çıkış
        """)
        choice = input(">> Seçimin: ")

        if choice == "0":
            break
        target = input("Hedef (IP ya da alan adı): ")

        if choice == "1":
            ping_target(target)
        elif choice == "2":
            dns_lookup(target)
        elif choice == "3":
            port_scan(target)
        elif choice == "4":
            basic_whois(target)
        elif choice == "5":
            http_headers(target)
        else:
            print("Geçersiz seçim.")

        input("\nDevam etmek için Enter'a bas...")

if __name__ == "__main__":
    main()
