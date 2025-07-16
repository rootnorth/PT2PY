# pt2py_recon_gui.py
# by @rootnorth (github)

import asyncio
import aiohttp
import dns.resolver
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.markdown import Markdown

console = Console()

ASCII_ART = r"""
######  #######  #####  ######  #     #    
#     #    #    #     # #     #  #   #     
#     #    #          # #     #   # #      
######     #     #####  ######     #       
#          #    #       #          #       
#          #    #       #          #       
#          #    ####### #          #       
                                           
                                   
#####  ######  ####   ####  #    # 
#    # #      #    # #    # ##   # 
#    # #####  #      #    # # #  # 
#####  #      #      #    # #  # # 
#   #  #      #    # #    # #   ## 
#    # ######  ####   ####  #    # 
                                   
"""

class PassiveRecon:
    def __init__(self, domain, securitytrails_key=None):
        self.domain = domain
        self.securitytrails_key = securitytrails_key
        self.subdomains = set()

    async def crtsh(self):
        url = f"https://crt.sh/?q=%25.{self.domain}&output=json"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=15) as resp:
                    if resp.status != 200:
                        console.print(f"[red][crt.sh][/red] HTTP {resp.status} hatası.")
                        return
                    data = await resp.json()
                    for entry in data:
                        names = entry.get("name_value", "")
                        for n in names.split("\n"):
                            n = n.strip()
                            if n.endswith(self.domain):
                                self.subdomains.add(n.lower())
                    console.print(f"[green][crt.sh][/green] {len(self.subdomains)} alt domain bulundu.")
            except Exception as e:
                console.print(f"[red][crt.sh][/red] Hata: {e}")

    async def securitytrails(self):
        if not self.securitytrails_key:
            console.print("[yellow][SecurityTrails][/yellow] API anahtarı yok, geçiliyor.")
            return
        url = f"https://api.securitytrails.com/v1/domain/{self.domain}/subdomains"
        headers = {"APIKEY": self.securitytrails_key}
        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with session.get(url, timeout=15) as resp:
                    if resp.status != 200:
                        console.print(f"[red][SecurityTrails][/red] HTTP {resp.status} hatası.")
                        return
                    data = await resp.json()
                    subs = data.get("subdomains", [])
                    for sub in subs:
                        full_sub = f"{sub}.{self.domain}"
                        self.subdomains.add(full_sub.lower())
                    console.print(f"[green][SecurityTrails][/green] {len(subs)} alt domain eklendi.")
            except Exception as e:
                console.print(f"[red][SecurityTrails][/red] Hata: {e}")

    async def run(self):
        await self.crtsh()
        await self.securitytrails()
        return sorted(self.subdomains)

class ActiveRecon:
    def __init__(self, domain, subdomains):
        self.domain = domain
        self.subdomains = subdomains
        self.alive_subs = []

    async def dns_check(self, sub, resolver):
        try:
            answers = resolver.resolve(sub, 'A')
            if answers:
                return sub
        except:
            return None

    async def http_check(self, sub, session):
        url = f"http://{sub}"
        try:
            async with session.get(url, timeout=5) as resp:
                if resp.status < 400:
                    return sub
        except:
            return None

    async def check_subdomain(self, sub, resolver, session):
        dns_result = await self.dns_check(sub, resolver)
        if dns_result:
            http_result = await self.http_check(sub, session)
            if http_result:
                return sub
        return None

    async def run(self):
        resolver = dns.resolver.Resolver()
        resolver.lifetime = 3
        resolver.timeout = 3

        async with aiohttp.ClientSession() as session:
            tasks = []
            for sub in self.subdomains:
                tasks.append(self.check_subdomain(sub, resolver, session))
            results = await asyncio.gather(*tasks)
            self.alive_subs = [r for r in results if r]
        console.print(f"[green][Active Recon][/green] {len(self.alive_subs)} aktif alt domain bulundu.")
        return self.alive_subs

def clear():
    import os
    os.system("cls" if os.name == "nt" else "clear")

async def main_menu():
    while True:
        clear()
        console.print(Panel.fit(Align.center(Text(ASCII_ART, style="bold cyan")), title="[bold yellow]PT2PY Recon Hub[/bold yellow]"))
        table = Table(title="Menü", show_header=True, header_style="bold magenta")
        table.add_column("Seçenek", justify="center")
        table.add_column("Açıklama")
        table.add_row("1", "Passive Recon (crt.sh + SecurityTrails)")
        table.add_row("2", "Active Recon (DNS + HTTP Kontrol)")
        table.add_row("0", "Çıkış")
        console.print(table)

        choice = Prompt.ask("Seçiminiz", choices=["0","1","2"], default="0")

        if choice == "1":
            domain = Prompt.ask("Hedef domain")
            st_key = Prompt.ask("SecurityTrails API key (opsiyonel)", default="")
            st_key = st_key if st_key.strip() else None
            passive = PassiveRecon(domain, st_key)
            subs = await passive.run()
            if subs:
                subs_table = Table(title=f"{domain} Alt Domainleri", show_lines=True)
                subs_table.add_column("No", justify="right")
                subs_table.add_column("Alt Domain")
                for idx, sub in enumerate(subs, 1):
                    subs_table.add_row(str(idx), sub)
                console.print(subs_table)
            else:
                console.print("[yellow]Alt domain bulunamadı veya hata oluştu.[/yellow]")
            input("Devam etmek için Enter'a basın...")

        elif choice == "2":
            domain = Prompt.ask("Hedef domain")
            subs_input = Prompt.ask("Alt domain listesi (virgülle ayrılmış ya da boş bırak)")
            if subs_input.strip():
                subs = [s.strip() for s in subs_input.split(",") if s.strip()]
                active = ActiveRecon(domain, subs)
                alive = await active.run()
                if alive:
                    alive_table = Table(title="Canlı Alt Domainler", show_lines=True)
                    alive_table.add_column("No", justify="right")
                    alive_table.add_column("Alt Domain")
                    for idx, sub in enumerate(alive, 1):
                        alive_table.add_row(str(idx), sub)
                    console.print(alive_table)
                else:
                    console.print("[yellow]Canlı alt domain bulunamadı.[/yellow]")
            else:
                console.print("[red]Alt domain listesi boş![/red]")
            input("Devam etmek için Enter'a basın...")

        elif choice == "0":
            console.print("[bold red]Çıkış yapılıyor...[/bold red]")
            sys.exit()

if __name__ == "__main__":
    try:
        asyncio.run(main_menu())
    except KeyboardInterrupt:
        console.print("\n[red]Program sonlandırıldı.[/red]")
