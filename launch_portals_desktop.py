#!/usr/bin/env python3
"""
César+ Immediate Portal Launcher
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
        
        # Open first tab
        page = context.new_page()
        print(f"🔗 Opening: {urls[0]}")
        page.goto(urls[0])
        
        # Open other tabs
        for url in urls[1:]:
            print(f"🔗 Opening tab: {url}")
            tab = context.new_page()
            tab.goto(url)
            
        print("\n🏆 ALL PORTALS LAUNCHED SUCCESSFULLY ON YOUR SCREEN!")
        print("Keep this terminal process running to keep the browser window open.")
        print("Once you are ready to close the browser, press Ctrl+C here.")
        
        # Keep process alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nClosing browser...")
            browser.close()

if __name__ == "__main__":
    main()
