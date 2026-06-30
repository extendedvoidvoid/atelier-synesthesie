#!/usr/bin/env python3
"""
César+ Playwright Form-Filling Co-pilot (Security-First Edition)
Launches an interactive browser session and auto-types your startup specs
and private administrative details into active form fields on autopilot.
"""

import sys
import time
import json
from pathlib import Path

# Try importing Playwright
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("⚠️ 'playwright' Python library not found. Installing it for this session...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    from playwright.sync_api import sync_playwright

# Core public content library mapped to numbers
CONTENT_MAP = {
    "1": {
        "title": "English Short Summary",
        "text": "Our proprietary 'CraftCut' pipeline for editorial video creation at the forefront of content creation, preserving cultural heritage, fashion, design, and French craftsmanship through automated vertical video essays."
    },
    "2": {
        "title": "French Short Summary (Résumé)",
        "text": "Notre pipeline propriétaire 'CraftCut' dédié à la création de vidéos éditoriales à l'avant-garde de la création de contenu, valorisant le patrimoine, le design, la mode et le savoir-faire des Artisans et Ouvriers de France."
    },
    "3": {
        "title": "English Master Pitch",
        "text": "Atelier Synesthésie is an automated, high-fidelity vertical video essay generator developed at Station F, Paris. The platform transforms static cultural archives—including Apple Music animated artworks, haute couture fashion layouts, architectural designs, and high-precision visual archives of French craftsmanship ('Les Ouvriers de France')—into immersive, high-end short-form documentaries. Our engine uses a multi-agent framework to handle deep historical research, multi-language voiceover synthesis, and professional-grade typography. We are dedicated to putting the human hands of craftsmanship and the beauty of global design back in the digital spotlight on TikTok, YouTube, and Instagram."
    },
    "4": {
        "title": "French Master Pitch (Vision)",
        "text": "Développé au sein de Station F, Atelier Synesthésie est un moteur automatisé de génération d'essais vidéo verticaux haute fidélité. Notre mission est de faire revivre les archives statiques et artistiques (pochettes animées Apple Music, photographies de haute couture, plans d'architecte) et de mettre en valeur l'excellence du geste artisanal français d'exception ('Les Ouvriers de France') auprès des nouvelles générations au format mobile 9:16. Grâce à une architecture multi-agents autonomes, nous gérons la recherche historique exhaustive, la synthèse vocale polyglotte et le calage typographique de précision."
    },
    "5": {
        "title": "Technical Case & Token Workload",
        "text": "Our multi-agent architecture utilizes parallel, high-context historical sourcing (consuming ~15,000 input tokens per run of retrieved web contexts) combined with custom, dynamic translation duration bounding algorithms across 7 languages simultaneously (~12,000 output tokens per run). Operating in batches of 50 assets daily (50 assets x 7 languages = 350 final localized videos), our production pipeline demands an estimated monthly volume of 64.3 Million tokens, requiring high-tier enterprise API keys, robust rate limits, and custom credit line scaling."
    },
    "6": {
        "title": "Legal & Business Structure",
        "text": "Registered under French Auto-Entrepreneur (Micro-Entreprise) status. Currently scaling the MVP locally utilizing local M3 Max Apple Silicon hardware-accelerated encoders (hevc_videotoolbox) to achieve zero-cost rendering, prior to scaling parallel rendering on cloud container clusters (Google Cloud Run)."
    },
    "7": {
        "title": "Creator's Profile (César)",
        "text": "Our founder’s philosophy is defined by direct execution over corporate self-promotion. We choose not to maintain traditional, buzzword-heavy LinkedIn profiles, choosing instead to let our active codebase, our live high-fidelity website showcase, and our public YouTube vertical feeds speak for themselves. César is an experienced creative systems engineer with decades of background in systems architecture, local GPU engineering, and high-end video compilation pipelines, now focused entirely on building CraftCut’s sovereign media infrastructure."
    }
}

def load_private_details():
    """Loads private details from local JSON if available."""
    private_file = Path(__file__).parent / "PRIVATE_DETAILS.json"
    details = {}
    
    if private_file.exists():
        try:
            with open(private_file, "r") as f:
                data = json.load(f)
                
                # Check if values are filled
                if data.get("full_name") and "YOUR_FULL_NAME" not in data["full_name"]:
                    details["8"] = {"title": "Full Name", "text": data["full_name"]}
                if data.get("address") and "YOUR_STREET_ADDRESS" not in data["address"]:
                    details["9"] = {"title": "Physical Address", "text": data["address"]}
                if data.get("phone_number") and "YOUR_CONTACT_PHONE" not in data["phone_number"]:
                    details["10"] = {"title": "Phone Number", "text": data["phone_number"]}
        except Exception as e:
            print(f"⚠️ Error loading PRIVATE_DETAILS.json: {e}")
            
    return details

def display_menu(private_details):
    print("\n" + "=" * 56)
    print("📋 CRAFTCUT CO-PILOT FORM FILLER ACTIVE")
    print("=" * 56)
    print("Instructions:")
    print("1. Click on any text input box in the browser window.")
    print("2. Type the number in your terminal and press ENTER.")
    print("3. The script will instantly type the text into the active field.")
    print("=" * 56 + "\n")
    
    # Public Specs
    print("--- 📚 Public & Brand Specifications ---")
    for key, value in CONTENT_MAP.items():
        print(f"  [{key}] {value['title']}")
        
    # Private Admin Details
    print("\n--- 🔐 Private & Administrative Details ---")
    if private_details:
        for key, value in private_details.items():
            print(f"  [{key}] {value['title']}")
    else:
        print("  ⚠️ PRIVATE_DETAILS.json is empty or not configured.")
        print("     Edit the local file privately to add your Name, Address, and Phone.")
        
    print("\n  [Q] Quit script")
    print("-" * 56)

def run():
    default_url = "https://foundershub.startups.microsoft.com"
    print(f"\nEnter target application URL (default: {default_url}):")
    target_url = input("> ").strip() or default_url
    
    if not target_url.startswith("http"):
        target_url = "https://" + target_url

    # Check and load local details
    private_details = load_private_details()
    combined_content = {**CONTENT_MAP, **private_details}

    with sync_playwright() as p:
        print("\n🌐 Launching Chromium browser...")
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        page.goto(target_url)
        
        while True:
            # Re-read private details on each loop to allow hot-reloads if user edits the file live!
            current_private = load_private_details()
            combined_content = {**CONTENT_MAP, **current_private}
            
            display_menu(current_private)
            choice = input("Paste content # > ").strip()
            
            if choice.lower() == 'q':
                print("\n👋 Closing browser. Good luck with your application!")
                browser.close()
                break
                
            if choice in combined_content:
                selected_item = combined_content[choice]
                text_to_type = selected_item["text"]
                print(f"\n✍️ Typing '{selected_item['title']}'...")
                
                try:
                    # Focus active element, clear field, and type smoothly
                    page.evaluate("() => { const el = document.activeElement; if (el) { el.value = ''; } }")
                    page.keyboard.insert_text(text_to_type)
                    print("✅ Success! Text pasted.")
                except Exception as e:
                    print(f"⚠️ Playwright Action Failed: {e}")
                    print("Make sure you have clicked inside an input box in the browser before choosing a number!")
            else:
                print("❌ Invalid selection. Please choose a number from the menu.")
            
            time.sleep(0.5)

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nExiting script...")
