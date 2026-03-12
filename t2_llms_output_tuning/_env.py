import os
from pathlib import Path


def load_dotenv() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        key, _, value = s.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and os.environ.get(key) in (None, ""):
            os.environ[key] = value
