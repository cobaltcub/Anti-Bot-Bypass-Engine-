import os
import json
from rich.console import Console
import config
from cookie_refresh import refresh_clearance_tokens
from bypass_engine import AntiBotBypassEngine

console = Console()

def load_cached_session() -> dict | None:
    """Reads saved session details from the local JSON store if available."""
    if os.path.exists(config.SESSION_FILE):
        try:
            with open(config.SESSION_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            console.print("[bold red][!] Session cache corrupted. Regenerating...[/bold red]")
    return None

def save_session_cache(data: dict):
    """Persists fresh browser token pools into the local storage file."""
    with open(config.SESSION_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def main():
    # Check if existing data available and use it if it is.
    session_data = load_cached_session()

    if not session_data:
        console.print("[bold yellow][*] No active session found. Invoking Playwright worker...[/bold yellow]")
        session_data = refresh_clearance_tokens()
        
        if session_data:
            save_session_cache(session_data)
            console.print("[bold green][+] Saved fresh session token cache to disk.[/bold green]")
        else:
            console.print("[bold red][-] Critical: Token generation routine timed out.[/bold red]")
            return

    engine = AntiBotBypassEngine(session_data)
    html_content = engine.fetch_protected_content(config.TARGET_URL)

    if html_content is None:
        console.print("[bold yellow][*] Cached tokens failed/expired. Auto-refreshing session...[/bold yellow]")
        session_data = refresh_clearance_tokens()
        
        if session_data:
            save_session_cache(session_data)
            engine = AntiBotBypassEngine(session_data)
            html_content = engine.fetch_protected_content(config.TARGET_URL)

    if html_content:
        with open("scraped_data.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        console.print("[bold yellow][*] Output compiled successfully into scraped_data.html[/bold yellow]")

if __name__ == "__main__":
    main()