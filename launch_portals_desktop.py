#!/usr/bin/env python3
"""
César+ Resilient Portal Launcher
Launches Chromium on your desktop and opens all 4 credit application forms.
"""

import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    from playwright.sync_api import sync_playwright

def main():
    urls = [
        "https://www.byteplus.com/en/activity/vstart",
        "https://portal.startups.microsoft.com/signup",
        "https://cloud.google.com/startup/apply",
        "https://console.aws.amazon.com/activate/home/#/apply"
    ]

    with sync_playwright() as p:
        print("🌐 Launching Chromium browser on your desktop...")
        # Start browser in maximized, non-headless mode
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        
        # Open first tab (resilient parameters)
        page = context.new_page()
        print(f"🔗 Opening: {urls[0]}...")
        try:
            page.goto(urls[0], wait_until="domcontentloaded", timeout=60000)
            print("  ✓ BytePlus loaded!")
        except Exception as e:
            print(f"  ⚠️ Warning loading BytePlus: {e}. Proceeding to other tabs...")
        
        # Open other tabs (resilient parameters)
        for url in urls[1:]:
            print(f"🔗 Opening tab: {url}...")
            try:
                tab = context.new_page()
                tab.goto(url, wait_until="domcontentloaded", timeout=60000)
                print(f"  ✓ Loaded!")
            except Exception as e:
                print(f"  ⚠️ Warning loading tab {url}: {e}. Proceeding...")
            
        print("\n🏆 PORTALS COMPLETED ON YOUR SCREEN!")
        print("Keep this process running to keep the browser window active.")
        print("Once you are finished, press Ctrl+C here in the terminal.")
        
        # Keep process alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nClosing browser...")
            browser.close()

if __name__ == "__main__":
    main()
