import os
import json
import time
from datetime import datetime
from utils.quota import check_quota_status

START_TIME = time.time()
USAGE_LOG_PATH = "resources/usage_log.json"
ERROR_LOG_PATH = "resources/error_log.json"

def get_uptime():
    seconds = int(time.time() - START_TIME)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

def get_today_usage():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    if os.path.exists(USAGE_LOG_PATH):
        with open(USAGE_LOG_PATH, "r") as f:
            usage = json.load(f)
        return usage.get(today, 0)
    return 0

def get_error_count():
    if os.path.exists(ERROR_LOG_PATH):
        with open(ERROR_LOG_PATH, "r") as f:
            logs = json.load(f)
        return len(logs)
    return 0

def get_status_report():
    return {
        "uptime": get_uptime(),
        "quota_status": check_quota_status(),
        "characters_used_today": get_today_usage(),
        "error_log_entries": get_error_count()
    }
