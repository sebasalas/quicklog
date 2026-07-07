# quicklog

Minimal CLI for quick, timestamped notes. You type, it saves — each entry stamped with `HH:MM:SS` and appended to a daily Markdown file (`quicklog_YYYYMMDD.md`) in a directory you choose.

Plain text, no database, no dependencies beyond the Python standard library.

## Setup

```bash
# Add an alias to ~/.zshrc (or ~/.bashrc)
alias log='python3 /path/to/quicklog.py'

source ~/.zshrc
```

On first run it asks where to save your notes and remembers it. That's it.

## Usage

```
log
> deployed v1.2 to staging
Saved.

> /show
```

Anything that isn't a command is saved as a note for the current day. Use arrow keys to edit the line and ↑/↓ to recall earlier entries from the session.

## Commands

| Command | Description |
|---|---|
| `/show [date]` | Show a day's notes. Date: `today` (default), `yesterday`, or `YYYY-MM-DD` |
| `/m` | Multiline entry — write several lines, an empty line saves it |
| `/list` | List every day that has notes |
| `/delete` | Delete the last entry of today (asks to confirm) |
| `/where` | Print the current notes directory |
| `/settings` | Change the notes directory |
| `/help` | Show available commands |
| `Ctrl+C` | Exit |

## How notes are stored

Each entry is one timestamped block, separated by a blank line:

```
14:32:10 deployed v1.2 to staging
14:35:01 note that spans
several lines from /m
```

Files stay flush-left and clean, so they read well in any Markdown viewer (Obsidian, VS Code, GitHub). When you run `/show`, long lines and multiline entries are aligned under the text for readability — that alignment is display-only and is never written to the file.

## Requirements

- Python 3 (standard library only)
- macOS or Linux — line editing and history rely on `readline`, which ships with Python on both

## Config

Your notes directory is stored in `~/.quicklog.json`.
