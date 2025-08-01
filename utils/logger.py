import json
from datetime import datetime

LOG_PATH = "resources/error_log.json"

def log_error(error_msg, context=None):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "error": error_msg,
        "context": context
    }

    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(entry)

        with open(LOG_PATH, "w") as f:
            json.dump(logs, f, indent=2)

    except Exception as e:
        print(f"[Logger Error] Failed to log: {e}")
