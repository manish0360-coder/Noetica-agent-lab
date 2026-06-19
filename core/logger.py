import json
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path("data/agent_runs.jsonl")


def log_run(record: dict) -> None:
    """Append one structured run record to the JSONL log.
    Append-only — never overwrites existing data.
    One line per run: grep-able, pandas-loadable, replayable.
    """
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")