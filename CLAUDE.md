# Trend Letter Bot — Orchestrator

## System Overview
Auto-generates a Korean trend newsletter HTML from a Telegram trigger.
Five roles execute in strict sequence. Each role spec lives in `.claude/roles/`.

**Global constraints (apply to every role):**
- **Never pause mid-task to ask the user for confirmation.** Execute fully autonomously.
- **Telegram messages: exactly 2 per run** — start notification + completion with file attached. No in-between messages.
- All HTML visible content must be in Korean.
- Read today's date from the `currentDate` value in the system context.
- `bypassPermissions` is active — all tool calls are pre-authorized.
- Run independent operations (searches, image fetches, curl checks) **in parallel** wherever possible.

---

## TRIGGER

**Input:** Telegram message containing "트렌드 레터 만들어줘"

**On trigger — do exactly this:**
1. Send Telegram reply: `"트렌드 레터 제작 시작할게요! 완료되면 파일로 보내드릴게요 🙌"`
2. Execute roles in strict order: ROLE_1 → ROLE_2 → ROLE_3 → ROLE_4 → ROLE_5
3. On any unrecoverable failure: send one Telegram reply naming the failed role and the error

---

## ROLE SPECIFICATIONS

@.claude/roles/role1_style_analyst.md

@.claude/roles/role2_trend_researcher.md

@.claude/roles/role3_image_sourcer.md

@.claude/roles/role4_content_writer.md

@.claude/roles/role5_publisher.md

---

## GLOBAL PROHIBITIONS

❌ NO markdown code fences (` ```html `) in HTML output  
❌ NO meta-commentary in output (`"위 내용을 바탕으로..."` etc.)  
❌ NO CSS deviation from ROLE_1 extraction  
❌ NO trend data older than 14 days  
❌ NO unverified image URLs (every URL must return HTTP 200)  
❌ NO images from fewer than 3 distinct domains  
❌ NO placeholder `<div>` substituting for images — real `<img>` tags only  
❌ NO English visible text in rendered newsletter (CSS class names excepted)  
❌ NO mid-task Telegram messages asking for approval or confirmation  
❌ NO topics duplicating stories already in `references/`
