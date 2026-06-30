# 📑 CRAFTCUT FORM INTEGRATION SPECS & EMAIL DIRECTIVES
*Sovereign Interactive Connections & Local Forms Database Mapping*

This specification maps all active call-to-action (CTA) links, waitlists, and email targets on your live website, alongside how to leverage your local Tesla Pros database for dynamic channel-tracking.

---

## 📧 1. Live Website Form CTAs & Parameters

All interactive elements on your live website are now configured to send high-signal, pre-formatted leads directly to:
👉 **`extendedvoid.prod+craftcut@gmail.com`**

| CTA Button / Link | Page Location | Method / Payload | Subject / URL Mapping |
| :--- | :--- | :--- | :--- |
| **"Join the waitlist"** | Top Nav Pill (Floating) | `mailto` Link | `CraftCut - Waitlist Subscription` |
| **"View our initiatives"** | Hero Left (Primary) | Anchor Scroll | `#roadmap` |
| **"Explore the repository"**| Hero Center (Ghost) | Direct Link | `https://github.com/extendedvoidvoid/atelier-synesthesie` |
| **"Contact César"** | Phase 2 (HEC Card) | `onclick` Mailto | `CraftCut - HEC Admission Interest` |
| **"GitHub Link"** | Footer Left | Direct Link | `https://github.com/extendedvoidvoid/atelier-synesthesie` |

---

## 📂 2. Local Series-UID Forms Mapping (The Tesla Pros Connection)

Your local database file at `/Users/alexphoenix/Library/Containers/com.tesla.teslapros/Data/Documents/react-query/rq1_extendedvoid.prod@gmail.com_formsbyseriesuid.json` tracks specific form series-UID mappings.

### How to use this for Niche-Channel Attribution:
If you decide to scale to **hundreds of parallel vertical channels** (your video printing press model), you can track exactly which video, track, or fashion collection generated each subscriber:

1.  **Generate a Series-UID:** For each automated channel, generate or retrieve a unique series ID from your local JSON (e.g., `004bce9b-c9f2-4067-9854-9f098618a7fb` maps to ID `85480`).
2.  **Dynamic Parameter Injection:** Embed this Series-UID directly into your video overlays, descriptions, or local bio links.
3.  **Lead Attributions:** When a user clicks the link to subscribe or join the waitlist, pass the Series-UID parameter:
    `mailto:extendedvoid.prod+craftcut@gmail.com?subject=CraftCut%20-%20Waitlist%20Subscription%20[Series-004bce9b]`
4.  **Auto-Sorting:** This allows your local mail filters or your automated script (`agent_apply.py` or **Hermes**) to parse the incoming emails, match the Series-UID against your local JSON file, and automatically attribute the lead to the exact music or fashion channel on autopilot!
