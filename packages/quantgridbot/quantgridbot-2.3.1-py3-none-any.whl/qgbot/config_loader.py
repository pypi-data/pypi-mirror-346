import json
import logging
from pathlib import Path

def load_config(config_path: str = "config.json") -> dict:
    try:
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with path.open("r", encoding="utf-8") as f:
            config = json.load(f)
            logging.info(f"[CONFIG] Loaded from {config_path}")
            return config
    except Exception as e:
        logging.error(f"[CONFIG LOAD ERROR] {e}")
        raise
