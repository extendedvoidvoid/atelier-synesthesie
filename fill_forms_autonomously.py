#!/usr/bin/env python3
"""
César+ Autonomous Form-Filling Robot (Deep DOM-Mapping Edition)
Autonomously parses active application portals and pre-fills all fields
using your brand pitches and private credentials.
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

# Content Library
PORTALS = {
    "1": {
        "name": "BytePlus vStart",
        "url": "https://www.byteplus.com/en/activity/vstart"
    },
    "2": {
        "name": "Microsoft for Startups",
        "url": "https://portal.startups.microsoft.com/signup"
    },
    "3": {
        "name": "Google for Startups",
        "url": "https://cloud.google.com/startup/apply"
    },
    "4": {
        "name": "AWS Activate",
        "url": "https://console.aws.amazon.com/activate/home/#/apply"
    }
}

DATA_PAYLOAD = {
    "company_name": "CraftCut",
    "website": "https://extendedvoidvoid.github.io/atelier-synesthesie/",
    "youtube_channel": "https://youtube.com",
    "full_name": "César Cabrera",
    "address": "Paris, France",
    "phone": "+33 602081648",
    "email": "extendedvoid.prod+craftcut@gmail.com",
    "launch_date": "June 2026",
    "structure": "Auto-Entrepreneur (Micro-Entreprise)",
    "target_audience": "French and global luxury fashion houses (Chanel, LVMH, etc.) and design agencies looking to scale prestigious vertical narratives.",
    "short_summary": "Our proprietary 'CraftCut' pipeline for editorial video creation at the forefront of content creation, preserving cultural heritage, fashion, design, and French craftsmanship through automated vertical video essays.",
    "short_summary_fr": "Notre pipeline propriétaire 'CraftCut' dédié à la création de vidéos éditoriales à l'avant-garde de la création de contenu, valorisant le patrimoine, le design, la mode et le savoir-faire des Artisans et Ouvriers de France.",
    "master_pitch": "Atelier Synesthésie is an automated, high-fidelity vertical video essay generator developed at Station F, Paris. The platform transforms static cultural archives—including Apple Music animated artworks, haute couture fashion layouts, architectural designs, and high-precision visual archives of French craftsmanship ('Les Ouvriers de France')—into immersive, high-end short-form documentaries. Our engine uses a multi-agent framework to handle deep historical research, multi-language voiceover synthesis, and professional-grade typography. We are dedicated to putting the human hands of craftsmanship and the beauty of global design back in the digital spotlight on TikTok, YouTube, and Instagram.",
    "master_pitch_fr": "Développé au sein de Station F, Atelier Synesthésie est un moteur automatisé de génération d'essais vidéo verticaux haute fidélité. Notre mission est de faire revivre les archives statiques et artistiques (pochettes animées Apple Music, photographies de haute couture, plans d'architecte) et de mettre en valeur l'excellence du geste artisanal français d'exception ('Les Ouvriers de France') auprès des nouvelles générations au format mobile 9:16. Grâce à une architecture multi-agents autonomes, nous gérons la recherche historique exhaustive, la synthèse vocale polyglotte et le calage typographique de précision.",
    "tech_case": "Our multi-agent architecture utilizes parallel, high-context historical sourcing (consuming ~15,000 input tokens per run of retrieved web contexts) combined with custom, dynamic translation duration bounding algorithms across 7 languages simultaneously (~12,000 output tokens per run). Operating in batches of 50 assets daily (50 assets x 7 languages = 350 final localized videos), our production pipeline demands an estimated monthly volume of 64.3 Million tokens, requiring high-tier enterprise API keys, robust rate limits, and custom credit line scaling.",
    "founder_profile": "Our founder’s philosophy is defined by direct execution over corporate self-promotion. We choose not to maintain traditional, buzzword-heavy LinkedIn profiles, choosing instead to let our active codebase, our live high-fidelity website showcase, and our public YouTube vertical feeds speak for themselves. César is an experienced creative systems engineer with decades of background in systems architecture, local GPU engineering, and high-end video compilation pipelines, now focused entirely on building CraftCut’s sovereign media infrastructure."
}

def load_private_override():
    """Loads actual private details if populated in PRIVATE_DETAILS.json."""
    private_file = Path(__file__).parent / "PRIVATE_DETAILS.json"
    if private_file.exists():
        try:
            with open(private_file, "r") as f:
                data = json.load(f)
                if data.get("full_name") and "YOUR_FULL" not in data["full_name"]:
                    DATA_PAYLOAD["full_name"] = data["full_name"]
                if data.get("address") and "YOUR_STREET" not in data["address"]:
                    DATA_PAYLOAD["address"] = data["address"]
                if data.get("phone_number") and "YOUR_CONTACT" not in data["phone_number"]:
                    DATA_PAYLOAD["phone"] = data["phone_number"]
        except Exception as e:
            pass

def scan_and_fill_inputs(page):
    """Scans all input elements on the page and intelligently fills them."""
    print("\n⚡ Scanning form inputs on the active tab...")
    
    # Extract all textareas, inputs
    inputs = page.query_selector_all("input, textarea")
    filled_count = 0
    
    for input_element in inputs:
        # Skip hidden, submit, radio, checkbox, file inputs for text filling
        elem_type = input_element.get_attribute("type")
        if elem_type in ["hidden", "submit", "button", "radio", "checkbox", "file"]:
            continue
            
        # Get identifier tokens
        name_attr = (input_element.get_attribute("name") or "").lower()
        id_attr = (input_element.get_attribute("id") or "").lower()
        placeholder_attr = (input_element.get_attribute("placeholder") or "").lower()
        aria_label = (input_element.get_attribute("aria-label") or "").lower()
        
        # Check label text
        label_text = ""
        try:
            # Check if there is an associated label by ID
            if id_attr:
                label_el = page.query_selector(f"label[for='{id_attr}']")
                if label_el:
                    label_text = label_el.inner_text().lower()
        except:
            pass
            
        combined_tokens = f"{name_attr} {id_attr} {placeholder_attr} {aria_label} {label_text}"
        
        # Match variables and fill
        text_to_fill = ""
        
        # 1. Company Name
        if any(tok in combined_tokens for tok in ["company", "startup", "start-up", "enterprise", "organization", "nom de l", "société"]):
            if "website" not in combined_tokens and "site" not in combined_tokens:
                text_to_fill = DATA_PAYLOAD["company_name"]
                
        # 2. Website URL
        elif any(tok in combined_tokens for tok in ["website", "url", "site", "web"]):
            if "youtube" in combined_tokens:
                text_to_fill = DATA_PAYLOAD["youtube_channel"]
            else:
                text_to_fill = DATA_PAYLOAD["website"]
                
        # 3. Full Name
        elif any(tok in combined_tokens for tok in ["name", "nom", "prénom", "contact person", "founder"]):
            if "company" not in combined_tokens and "startup" not in combined_tokens:
                text_to_fill = DATA_PAYLOAD["full_name"]
                
        # 4. Email Address
        elif any(tok in combined_tokens for tok in ["email", "courriel", "adresse électronique"]):
            text_to_fill = DATA_PAYLOAD["email"]
            
        # 5. Phone Number
        elif any(tok in combined_tokens for tok in ["phone", "tel", "téléphone", "contact number", "mobile"]):
            text_to_fill = DATA_PAYLOAD["phone"]
            
        # 6. Physical Address
        elif any(tok in combined_tokens for tok in ["address", "adresse", "city", "ville", "location", "pays", "country"]):
            if "email" not in combined_tokens:
                text_to_fill = DATA_PAYLOAD["address"]
                
        # 7. Short Summary / Elevator Pitch
        elif any(tok in combined_tokens for tok in ["summary", "description", "elevator", "one-line", "pitch", "en une phrase"]):
            # Check page language to choose EN or FR summary
            if "fr" in page.url or "français" in page.content().lower():
                text_to_fill = DATA_PAYLOAD["short_summary_fr"]
            else:
                text_to_fill = DATA_PAYLOAD["short_summary"]
                
        # 8. Detailed/Master Pitch
        elif any(tok in combined_tokens for tok in ["long description", "detailed description", "what do you do", "solution", "vision"]):
            if "fr" in page.url or "français" in page.content().lower():
                text_to_fill = DATA_PAYLOAD["master_pitch_fr"]
            else:
                text_to_fill = DATA_PAYLOAD["master_pitch"]
                
        # 9. Technical Specs / Cloud Workload
        elif any(tok in combined_tokens for tok in ["tech", "architecture", "workload", "gpu", "tokens", "cloud", "api", "usage", "model"]):
            text_to_fill = DATA_PAYLOAD["tech_case"]
            
        # 10. Bio / Founder Profile
        elif any(tok in combined_tokens for tok in ["bio", "founder profile", "linkedin", "about you", "background"]):
            text_to_fill = DATA_PAYLOAD["founder_profile"]

        if text_to_fill:
            try:
                # Scroll into view, clear, and type
                input_element.scroll_into_view_if_needed()
                input_element.focus()
                page.evaluate("(el) => { el.value = ''; }", input_element)
                input_element.type(text_to_fill, delay=30)
                filled_count += 1
                print(f"  ✓ Filled field (Match: '{name_attr or id_attr or label_text[:15]}')")
            except Exception as e:
                pass
                
    print(f"✨ Scanning completed. Auto-filled {filled_count} inputs.")

def main():
    load_private_override()
    
    print("\n" + "=" * 56)
    print("🤖 CÉSAR+ AUTONOMOUS APPLICATION ROBOT ACTIVE")
    print("=" * 56)
    print("Select the portal you want me to navigate to and automate:")
    print("-" * 56)
    for k, v in PORTALS.items():
        print(f"  [{k}] {v['name']} ({v['url']})")
    print("  [Q] Exit")
    print("-" * 56)
    
    choice = input("Select Portal # > ").strip()
    if choice.lower() == 'q' or choice not in PORTALS:
        print("Exiting...")
        sys.exit(0)
        
    portal = PORTALS[choice]
    
    with sync_playwright() as p:
        print(f"\n🌐 Launching Chromium browser for {portal['name']}...")
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        page.goto(portal["url"])
        
        print("\n" + "=" * 56)
        print("🔓 PORTAL OPENED ON YOUR SCREEN!")
        print("=" * 56)
        print("Please follow these steps:")
        print("1. Log in or sign up to your account on the opened browser window.")
        print("2. Navigate to the actual application/registration form page.")
        print("3. ONCE YOU ARE ON THE APPLICATION FORM, press ENTER in this terminal.")
        print("   I will immediately take over and fill out the entire page for you!")
        print("=" * 56 + "\n")
        
        input("Press ENTER once you are logged in and ready to autofill... ")
        
        # Take over and scan/fill
        scan_and_fill_inputs(page)
        
        print("\n" + "=" * 56)
        print("🏆 AUTOPILOT FORM FILLING COMPLETED!")
        print("=" * 56)
        print("Please review the fields in the browser window:")
        print("1. Confirm all text fields and details are accurate.")
        print("2. Complete any manual dropdowns, checkboxes, or file uploads.")
        print("3. When you are 100% satisfied, click 'SUBMIT' directly on the browser!")
        print("=" * 56 + "\n")
        
        print("Press ENTER in the terminal to close the browser once you are finished.")
        input("> ")
        browser.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting robot...")
