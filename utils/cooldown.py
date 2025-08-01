import json
import os

COOLDOWN_FILE = "resources/cooldown.json"

def is_translation_enabled():
    if not os.path.exists(COOLDOWN_FILE):
        return True  # Default to enabled
    with open(COOLDOWN_FILE, "r") as f:
        state = json.load(f)
    return state.get("enabled", True)

def set_translation_enabled(enabled: bool):
    with open(COOLDOWN_FILE, "w") as f:
        json.dump({"enabled": enabled}, f, indent=2)
