import json
import os
from datetime import datetime

USAGE_LOG_PATH = "resources/usage_log.json"
SOFT_THRESHOLD = 400_000
HARD_LIMIT = 490_000

def log_usage(char_count):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    usage = {}

    if os.path.exists(USAGE_LOG_PATH):
        with open(USAGE_LOG_PATH, "r") as f:
            usage = json.load(f)

    usage[today] = usage.get(today, 0) + char_count

    with open(USAGE_LOG_PATH, "w") as f:
        json.dump(usage, f, indent=2)

def check_quota_status():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    if os.path.exists(USAGE_LOG_PATH):
        with open(USAGE_LOG_PATH, "r") as f:
            usage = json.load(f)
        used = usage.get(today, 0)
        if used >= HARD_LIMIT:
            return "HARD_LIMIT"
        elif used >= SOFT_THRESHOLD:
            return "SOFT_THRESHOLD"
    return "OK"
