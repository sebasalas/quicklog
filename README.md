# quicklog

Minimal CLI tool for quick timestamped notes. Each entry is saved with a timestamp (`HH:MM:SS`) in a daily markdown file (`quicklog_YYYYMMDD.md`).

## Setup

```bash
# Add alias to ~/.zshrc
alias log='python3 /path/to/quicklog.py'

# Reload shell
source ~/.zshrc
```

On first run, you will be prompted to enter the directory where notes will be saved.

## Usage

```
log
> your note here
> another note
```

## Commands

| Command | Description |
|---|---|
| `/show [date]` | Show notes. Date: `today`, `yesterday`, or `YYYY-MM-DD` |
| `/list` | List all days with notes |
| `/m` | Multiline mode — write lines, empty line to save |
| `/where` | Display current notes location |
| `/settings` | Change the notes directory |
| `/help` | Show available commands |
| `Ctrl+C` | Exit |

## Config

Settings are stored in `~/.quicklog.json`.
