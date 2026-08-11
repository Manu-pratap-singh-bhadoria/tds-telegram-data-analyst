import os
import json
from datetime import datetime


LOG_FILE = os.path.join("logs", "run.jsonl")

os.makedirs("logs", exist_ok=True)


def write_log(question, tool, result):

    entry = {
        "time": datetime.utcnow().isoformat(),
        "question": question,
        "tool": tool,
        "result": result
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(
            json.dumps(entry, default=str)
            + "\n"
        )