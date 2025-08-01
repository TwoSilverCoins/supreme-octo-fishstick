# translator.py

import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
LOCATION = "global"  # ISO 3166 region code
USAGE_LOG_PATH = "resources/usage_log.json"
ERROR_LOG_PATH = "resources/error_log.json"

def log_usage(char_count):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    try:
        if os.path.exists(USAGE_LOG_PATH):
            with open(USAGE_LOG_PATH, "r") as f:
                usage = json.load(f)
        else:
            usage = {}

        usage[today] = usage.get(today, 0) + char_count

        with open(USAGE_LOG_PATH, "w") as f:
            json.dump(usage, f, indent=2)

    except Exception as e:
        print(f"[USAGE LOG ERROR] {e}")

def log_error(error_msg, text, target_lang):
    error_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "error": error_msg,
        "text": text,
        "target_lang": target_lang
    }
    try:
        if os.path.exists(ERROR_LOG_PATH):
            with open(ERROR_LOG_PATH, "r") as f:
                errors = json.load(f)
        else:
            errors = []

        errors.append(error_entry)

        with open(ERROR_LOG_PATH, "w") as f:
            json.dump(errors, f, indent=2)

    except Exception as e:
        print(f"[ERROR LOG FAILURE] {e}")

def translate(text, target_lang, source_lang="auto"):
    if not text.strip():
        return "⚠️ Empty message received."

    url = f"https://translation.googleapis.com/v3/projects/{PROJECT_ID}/locations/{LOCATION}:translateText"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [text],
        "mimeType": "text/plain",
        "sourceLanguageCode": source_lang,
        "targetLanguageCode": target_lang
    }
    params = {"key": GOOGLE_API_KEY}

    try:
        response = requests.post(url, headers=headers, params=params, json=payload)
        response.raise_for_status()
        result = response.json()
        translated_text = result["translations"][0]["translatedText"]

        # Track usage
        log_usage(len(text))

        return translated_text

    except requests.exceptions.HTTPError as http_err:
        log_error(f"HTTPError: {http_err}", text, target_lang)
        return "⚠️ Translation failed due to API error."

    except Exception as e:
        log_error(f"GeneralError: {e}", text, target_lang)
        return "⚠️ Translation failed due to internal error."
