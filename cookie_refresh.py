import time
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import config

def refresh_clearance_tokens() -> dict | None:
    print("[*] Launching ephemeral Playwright instance...")
    
    with Stealth().use_sync(sync_playwright()) as p:
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        
        print(f"[*] Navigating to target to clear anti-bot challenges...")
        try:
            page.goto(config.TARGET_URL, timeout=30000)
        except Exception as e:
            print(f"[-] Navigation Error: {e}")
            browser.close()
            return None
        
        cf_clearance = None
        timeout = 15
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            cookies = context.cookies()
            cf_clearance = next((c for c in cookies if c['name'] == 'cf_clearance'), None)
            if cf_clearance:
                print("[+] Successfully acquired cf_clearance token!")
                break
            page.wait_for_timeout(500)
            
        if not cf_clearance:
            browser.close()
            return None
            
        browser_ua = page.evaluate("() => navigator.userAgent")
        
        cookies_dict = {c['name']: c['value'] for c in cookies}
        browser.close()
        
        return {
            "cookies": cookies_dict,
            "user_agent": browser_ua
        }