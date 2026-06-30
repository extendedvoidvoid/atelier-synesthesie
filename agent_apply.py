#!/usr/bin/env python3
"""
César+ Startup Application Assistant CLI
Automatically drafts high-fidelity answers to startup and credit application questions.
"""

import os
import sys
import json
from pathlib import Path

# Try importing requests for API calls
try:
    import requests
except ImportError:
    print("⚠️ 'requests' library not found. Installing it for this session...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
    import requests

def load_config():
    """Loads API keys from standard locations."""
    config = {}
    
    # 1. Search in local .env of the album-video-creator project
    env_path = Path("/Users/alexphoenix/projects/album-video-creator/.env")
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    config[k.strip().lower()] = v.strip().strip('"').strip("'")
                    
    # 2. Search in global config
    global_cfg = Path.home() / ".album_video_maker_config.json"
    if global_cfg.exists():
        try:
            with open(global_cfg, "r") as f:
                data = json.load(f)
                for k, v in data.items():
                    if k.lower() not in config:
                        config[k.lower()] = v
        except:
            pass
            
    return config

def main():
    folder = Path(__file__).parent
    prompt_file = folder / "AGENT_PROMPT.md"
    
    if not prompt_file.exists():
        print(f"❌ Could not find AGENT_PROMPT.md in {folder}")
        sys.exit(1)
        
    with open(prompt_file, "r") as f:
        system_prompt = f.read()
        
    config = load_config()
    api_key = config.get("openrouter_api_key") or config.get("gemini_api_key")
    
    if not api_key:
        print("⚠️ No API keys found in .env or ~/.album_video_maker_config.json.")
        print("Please configure 'openrouter_api_key' or 'gemini_api_key' to run automated answers.")
        sys.exit(1)

    print("\n========================================================")
    print("🤖 César+ Startup Application Assistant CLI Loaded")
    print("========================================================\n")
    print("Enter the application question you want to answer (Ctrl+D or Ctrl+Z to finish):")
    print("-" * 56)
    
    lines = []
    try:
        for line in sys.stdin:
            lines.append(line)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
        
    user_question = "".join(lines).strip()
    if not user_question:
        print("❌ Question cannot be empty.")
        sys.exit(1)
        
    print("\n🧠 Crafting high-fidelity response using Atelier Synesthésie context...")
    
    # Check if using OpenRouter or Direct Gemini
    if config.get("openrouter_api_key"):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {config['openrouter_api_key']}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "google/gemini-2.5-flash",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Write a professional response to this application question:\n\n\"{user_question}\""}
            ]
        }
    else:
        # Fallback to Direct Gemini
        gemini_key = config.get("gemini_api_key")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": f"Write a professional response to this application question:\n\n\"{user_question}\""}]}],
            "generationConfig": {"temperature": 0.7}
        }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        if r.status_code == 200:
            res = r.json()
            if "choices" in res:
                response_text = res["choices"][0]["message"]["content"].strip()
            elif "candidates" in res:
                response_text = res["candidates"][0]["content"]["parts"][0]["text"].strip()
            else:
                response_text = "⚠️ Error parsing model output."
                
            print("\n" + "=" * 56)
            print("✨ PERFECTLY DRAFTED RESPONSE:")
            print("=" * 56 + "\n")
            print(response_text)
            print("\n" + "=" * 56 + "\n")
        else:
            print(f"❌ API Call failed with status code {r.status_code}: {r.text}")
    except Exception as e:
        print(f"❌ Exception occurred: {e}")

if __name__ == "__main__":
    main()
