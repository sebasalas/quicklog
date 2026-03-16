#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

CONFIG_FILE = Path.home() / ".quicklog.json"


def load_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return None


def strip_quotes(s):
    if len(s) >= 2 and s[0] in ('"', "'") and s[-1] == s[0]:
        return s[1:-1]
    return s


def save_config(config):
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


def help():
    print("/show      Show today's notes")
    print("/where     Display current notes location")
    print("/settings  Change the notes directory")
    print("/help      Show this help")
    print("Ctrl+C     Exit")


def show(log_dir):
    filename = log_dir / datetime.now().strftime("quicklog_%Y%m%d.md")
    if not filename.exists():
        print("No notes today.")
    else:
        print(filename.read_text())


def settings(config):
    print(f"Current log dir: {config['log_dir']}")
    try:
        new_dir = input("New log dir (Enter to keep current): ").strip()
    except (KeyboardInterrupt, EOFError):
        return config
    if new_dir:
        path = Path(strip_quotes(new_dir)).expanduser()
        path.mkdir(parents=True, exist_ok=True)
        config["log_dir"] = str(path)
        save_config(config)
        print(f"Saved: {config['log_dir']}")
    return config


config = load_config()
if config is None:
    print("First run! Enter the directory where notes will be saved:")
    try:
        initial_dir = input("> ").strip()
    except (KeyboardInterrupt, EOFError):
        raise SystemExit
    path = Path(strip_quotes(initial_dir)).expanduser()
    path.mkdir(parents=True, exist_ok=True)
    config = {"log_dir": str(path)}
    save_config(config)
    print(f"Saved: {config['log_dir']}")

log_dir = Path(config["log_dir"])
log_dir.mkdir(parents=True, exist_ok=True)

while True:
    try:
        text = input("> ")
    except (KeyboardInterrupt, EOFError):
        break
    if not text.strip():
        continue
    if text.strip() == "/help":
        help()
        continue
    if text.strip() == "/where":
        print(log_dir)
        continue
    if text.strip() == "/show":
        show(log_dir)
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
