import json
from datetime import datetime

LOG_FILE = "run.jsonl"

def write_log(question, tool, result):
    entry = {
        "time": datetime.utcnow().isoformat(),
        "question": question,
        "tool": tool,
        "result": result
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")