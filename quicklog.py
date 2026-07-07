#!/usr/bin/env python3
import json
import readline  # noqa: F401 — enables cursor movement and history for input()
import shutil
import textwrap
from datetime import datetime, timedelta
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
    print("/show [date]  Show notes (date: today, yesterday, YYYY-MM-DD)")
    print("/list         List all days with notes")
    print("/delete       Delete last entry of today")
    print("/where        Display current notes location")
    print("/settings     Change the notes directory")
    print("/help         Show this help")
    print("Ctrl+C        Exit")
    print("(empty line to save multiline note)")


def parse_date(arg):
    if not arg or arg == "today":
        return datetime.now()
    if arg == "yesterday":
        return datetime.now() - timedelta(days=1)
    try:
        return datetime.strptime(arg, "%Y-%m-%d")
    except ValueError:
        return None


def format_entry(entry, indent):
    # Wrap to terminal width so soft-wrapped lines also align under the text.
    width = max(shutil.get_terminal_size((80, 20)).columns, len(indent) + 20)
    lines = entry.split("\n")
    wrapped = [
        textwrap.fill(
            lines[0], width=width, subsequent_indent=indent,
            break_long_words=False, break_on_hyphens=False,
        )
    ]
    for line in lines[1:]:
        wrapped.append(
            textwrap.fill(
                line, width=width, initial_indent=indent, subsequent_indent=indent,
                break_long_words=False, break_on_hyphens=False,
            )
        )
    return "\n".join(wrapped)


def show(log_dir, arg=""):
    date = parse_date(arg.strip())
    if date is None:
        print(f"Invalid date: {arg}. Use today, yesterday, or YYYY-MM-DD.")
        return
    filename = log_dir / date.strftime("quicklog_%Y%m%d.md")
    if not filename.exists():
        print(f"No notes for {date.strftime('%Y-%m-%d')}.")
    else:
        entries = filename.read_text().strip().split("\n\n")
        indent = " " * 9  # width of "HH:MM:SS " — aligns continuation lines under the text
        print()
        for entry in entries:
            entry = entry.strip()
            if entry:
                print(format_entry(entry, indent))
                print("─" * 40)
        print()


def delete_last(log_dir):
    filename = log_dir / datetime.now().strftime("quicklog_%Y%m%d.md")
    if not filename.exists():
        print("No notes today.")
        return
    entries = [e for e in filename.read_text().split("\n\n") if e.strip()]
    if not entries:
        print("No notes today.")
        return
    print(f"Delete this entry?\n\n  {entries[-1].strip()}\n\n[y/N] ", end="")
    try:
        confirm = input().strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        return
    if confirm == "y":
        filename.write_text("\n\n".join(entries[:-1]) + ("\n\n" if len(entries) > 1 else ""))
        print("Deleted.")


def list_notes(log_dir):
    files = sorted(log_dir.glob("quicklog_*.md"))
    if not files:
        print("No notes found.")
        return
    for f in files:
        date_str = f.stem.replace("quicklog_", "")
        try:
            date = datetime.strptime(date_str, "%Y%m%d")
            print(date.strftime("%Y-%m-%d"))
        except ValueError:
            print(f.name)


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


def read_multiline():
    print("… multiline mode — empty line to save, Ctrl+C to cancel")
    lines = []
    while True:
        try:
            line = input("  ")
        except (KeyboardInterrupt, EOFError):
            return None
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines) if lines else None


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

print("Type /help for commands.")
print()

while True:
    try:
        text = input("> ")
    except (KeyboardInterrupt, EOFError):
        break
    cmd = text.strip()
    if not cmd:
        continue
    if cmd == "/help":
        help()
        continue
    if cmd == "/where":
        print(log_dir)
        continue
    if cmd.startswith("/show"):
        arg = cmd[5:].strip()
        show(log_dir, arg)
        continue
    if cmd == "/delete":
        delete_last(log_dir)
        continue
    if cmd == "/list":
        list_notes(log_dir)
        continue
    if cmd == "/settings":
        config = settings(config)
        log_dir = Path(config["log_dir"])
        continue
    if cmd == "/m":
        note = read_multiline()
        if not note:
            continue
        text = note
    now = datetime.now()
    filename = log_dir / now.strftime("quicklog_%Y%m%d.md")
    line = now.strftime("%H:%M:%S") + " " + text
    with open(filename, "a") as f:
        f.write(line + "\n\n")
    print("Saved.")
    print()
