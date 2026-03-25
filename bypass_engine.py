# bypass_engine.py

import time
from curl_cffi import requests
from rich.console import Console
from rich.panel import Panel
import config

console = Console()

class AntiBotBypassEngine:
    def __init__(self, session_data: dict):
        self.session = requests.Session()
        
        self.session.impersonate = "chrome"
        
        headers = config.BASE_HEADERS.copy()
        headers["User-Agent"] = session_data["user_agent"]
        self.session.headers.update(headers)
        
        # Inject the active cookie pool dynamically
        for name, value in session_data["cookies"].items():
            self.session.cookies.set(name, value)

    def fetch_protected_content(self, url: str) -> str | None:
        console.print(f"[bold cyan][*] Sending request via curl_cffi client...[/bold cyan]")
        
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=15)
            elapsed = time.time() - start_time
            
            # Check if we encountered 403
            if response.status_code == 403 and "cf-challenge" in response.text.lower():
                console.print(Panel.fit(
                    "[bold red][-] Blocked by Cloudflare Challenge Page.[/bold red]\n"
                    "The cf_clearance token has expired or session context was invalidated.",
                    title="Access Denied"
                ))
                return None

            if response.status_code in [503, 403]:
                console.print(f"[bold red][-] Request failed with status code: {response.status_code}[/bold red]")
                return None

            response.raise_for_status()
            
            # chicken dinner!!
            console.print(Panel.fit(
                f"[bold green][+] Bypass Successful![/bold green]\n"
                f"Status Code: {response.status_code}\n"
                f"Response Time: {elapsed:.2f}s\n"
                f"Content Length: {len(response.text)} characters",
                title="Engine Output"
            ))
            return response.text

        except Exception as e:
            console.print(f"[bold red][-] Network/Error Exception: {e}[/bold red]")
            return None