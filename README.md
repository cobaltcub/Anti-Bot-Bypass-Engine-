# Modular Anti-Bot Bypass Engine

This is a clean, hybrid scraper architecture designed to handle annoying Cloudflare checks without destroying your system's performance. 

Instead of keeping a heavy, memory-hogging Chromium browser running 24/7 just to scrape data, this setup uses a "hot-swap" logic. It spins up a stealthy browser for 10 seconds to solve challenges, steals the `cf_clearance` cookie, dumps it into a local JSON file, and shuts the browser down. From there, a lightweight C-compiled HTTP client (`curl_cffi`) takes over to do high-speed requests using the saved tokens.

## Project Layout

* **`config.py`** - Central settings, target URLs, and where the session JSON path is defined.
* **`cookie_refresh.py`** - The automation worker. Uses Playwright (with the newer v2.x Stealth wrapper) to pull fresh cookies and the matching User-Agent.
* **`bypass_engine.py`** - The high-speed scraper machine. Uses `curl_cffi` to spoof Chrome TLS fingerprints.
* **`main.py`** - The main controller. Logic handles checking the cache, running requests, and auto-refreshing if a token expires mid-run.

## Getting Started

### 1. Install dependancies
First, make sure you install everything from the txt file and set up the playwright binaries.

```bash
pip install -r requirements.txt
playwright install chromium