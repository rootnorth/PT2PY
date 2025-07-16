# network_mapping.py
# by @rootnorth (github)

import subprocess
import platform

def run():
    print("=== Network Mapping & Fingerprinting ===")
    target = input("Hedef IP veya domain: ").strip()

    nmap_path = "nmap"  # Windows için path sorun olabilir, kullanıcıya bildirilebilir

    args = [nmap_path, "-A", "-T4", target]  # OS ve servis versiyon tespiti, hızlı tarama

    try:
        print(f"[*] {target} üzerinde kapsamlı nmap taraması başlatılıyor...")
        subprocess.run(args)
        print("[*] Tarama tamamlandı.")
    except FileNotFoundError:
        print("nmap bulunamadı! Lütfen nmap kurulu olduğundan emin olun.")
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    run()
