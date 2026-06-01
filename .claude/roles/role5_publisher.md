# ROLE_5 · PUBLISHER

**Purpose:** Write the completed newsletter HTML file to disk. ROLE_6 handles the Telegram completion message.

**Inputs:** Complete HTML string from ROLE_4

## Process

1. **Write file** to `output/trend_letter_{MMDD}.html` (UTF-8)
   - `{MMDD}` = zero-padded month+day from today's date (e.g., `0517` for May 17)
   - Overwrite silently if file already exists — do not prompt

2. **Confirm success** internally — pass `{MMDD}` and today's date `{YYYY.MM.DD}` to ROLE_6 (no Vol number — issues are dated, not numbered)

## Failure Handling
- File write failure → send Telegram error message with attempted path and error details, then stop
