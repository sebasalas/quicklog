# quicklog

Minimal CLI tool for quick timestamped notes. Each entry is saved with a timestamp (`HH:MM:SS`) in a daily markdown file (`quicklog_YYYYMMDD.md`).

## Setup

```bash
# Add alias to ~/.zshrc
alias log='python3 /path/to/log.py'

# Reload shell
source ~/.zshrc
```

## Usage

```
log
> your note here
> another note
```

Notes are saved to the configured directory. Default: `~/Documents/obsidian_default/45 - Quicklog`.

## Commands

| Command | Description |
|---|---|
| `/settings` | Change the notes directory |
| `Ctrl+C` | Exit |

## Config

Settings are stored in `~/.quicklog.json`.
