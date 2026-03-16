#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

CONFIG_FILE = Path.home() / ".quicklog.json"
DEFAULT_DIR = Path("/Users/sebas/Documents/obsidian_default/45 - Quicklog")


def load_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {"log_dir": str(DEFAULT_DIR)}


def save_config(config):
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


def settings(config):
    print(f"Current log dir: {config['log_dir']}")
    try:
        new_dir = input("New log dir (Enter to keep current): ").strip()
    except (KeyboardInterrupt, EOFError):
        return config
    if new_dir:
        path = Path(new_dir).expanduser()
        path.mkdir(parents=True, exist_ok=True)
        config["log_dir"] = str(path)
        save_config(config)
        print(f"Saved: {config['log_dir']}")
    return config


config = load_config()
log_dir = Path(config["log_dir"])
log_dir.mkdir(parents=True, exist_ok=True)

print("Type your note and press Enter. /settings to configure. Ctrl+C to exit.")

while True:
    try:
        text = input("> ")
    except (KeyboardInterrupt, EOFError):
        break
    if not text.strip():
        continue
    if text.strip() == "/settings":
        config = settings(config)
        log_dir = Path(config["log_dir"])
        continue
    now = datetime.now()
    filename = log_dir / now.strftime("quicklog_%Y%m%d.md")
    line = now.strftime("%H:%M:%S") + " " + text
    with open(filename, "a") as f:
        f.write(line + "\n\n")
