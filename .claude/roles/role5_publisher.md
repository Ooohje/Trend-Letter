# ROLE_5 · PUBLISHER

**Purpose:** Write the completed HTML file to disk and notify the user via Telegram.

**Inputs:** Complete HTML string from ROLE_4

## Process

1. **Write file** to `output/trend_letter_{MMDD}.html` (UTF-8)
   - `{MMDD}` = zero-padded month+day from today's date (e.g., `0517` for May 17)
   - Overwrite silently if file already exists — do not prompt

2. **Send Telegram reply** in this exact format:
```
✅ 트렌드 레터 Vol.NN 완성됐어요!

📁 output/trend_letter_{MMDD}.html

📌 이번 호 4가지 트렌드:
1. [이모지] [trend title 1]
2. [이모지] [trend title 2]
3. [이모지] [trend title 3]
4. [이모지] [trend title 4]

🖼 이미지 소스: [domain1] + [domain2] + [domain3]
```

3. **Attach the HTML file** to the same Telegram reply using the `files` parameter of the reply tool

## Failure Handling
- File write failure → send Telegram error message with attempted path and error details
- Telegram send failure → output the file path to console; do not retry indefinitely
