# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the script

```bash
python3 quicklog.py
```

Or via the shell alias (after `source ~/.zshrc`):

```bash
log
```

## Architecture

Single-file script (`quicklog.py`) with no external dependencies. All logic runs at module level — no classes, no framework.

- **Config**: persisted in `~/.quicklog.json` as `{"log_dir": "/path/to/dir"}`. Loaded at startup; if missing, the user is prompted on first run.
- **Notes**: appended to `<log_dir>/quicklog_YYYYMMDD.md`, one file per day, each entry formatted as `HH:MM:SS <text>` followed by a blank line.
- **Commands**: handled inside the main `while True` input loop by matching `text.strip()`. Available: `/help`, `/show [date]`, `/list`, `/delete`, `/m`, `/where`, `/settings`.
  - `/show` accepts `today`, `yesterday`, or `YYYY-MM-DD`.
  - `/delete` removes the last entry of today's file after confirmation.
  - `/m` enters multiline mode — lines are collected until an empty line, then saved as a single timestamped entry.

## Alias

The script is invoked as `log` via an alias in `~/.zshrc`:

```bash
alias log='python3 /Users/sebas/code/personal/quicklog/quicklog.py'
```
