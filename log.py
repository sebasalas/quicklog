#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path

LOG_DIR = Path.home() / "logs"
LOG_DIR.mkdir(exist_ok=True)

print("Type your note and press Enter. Ctrl+C to exit.")

while True:
    try:
        text = input("> ")
    except (KeyboardInterrupt, EOFError):
        break
    if not text.strip():
        continue
    now = datetime.now()
    filename = LOG_DIR / now.strftime("%Y%m%d.txt")
    line = now.strftime("%H:%M:%S") + " " + text
    with open(filename, "a") as f:
        f.write(line + "\n")
