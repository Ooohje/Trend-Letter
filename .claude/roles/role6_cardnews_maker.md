# ROLE_6 · CARDNEWS_MAKER (Canva-native)

**Purpose:** Build the **"Trend News"** 6-page card news **inside Canva** by copying the approved master design and replacing its content, then write the Instagram caption and send the single Telegram completion message.

**There is NO HTML→PNG pipeline.** Do not run Python, Edge headless, or screenshot scripts. The card news lives entirely in Canva and is delivered as an edit link.

**Inputs:**
- Trend records from ROLE_2 (4 trends: category, headline, 3 body lines, references)
- Verified card-background image URLs from ROLE_3 (one per trend)
- `{MMDD}` and today's date `{YYYY.MM.DD}` from `currentDate`

**Outputs:**
- A Canva design (copy of the master) populated for this week → **edit link**
- `output/post_{MMDD}.txt` (Instagram caption)
- One Telegram completion message

---

## MASTER TEMPLATE (the approved look)

**Master design ID:** `DAHLSzY4WsQ` (Instagram portrait **1080×1350**, title wordmark "Trend News", dark editorial grid, blue accents, genZ lab logo top-right on every page).
Always **copy** this master — never edit the master itself. The copy inherits the exact layout, fonts, grid background, logo, and the reference-block styling the user finalized.

> Logo note: the genZ lab logo (asset `MAHLR2vMuLE`) is a **raster image** placed top-right on all 6 pages. Canva's editing API has **no recolor/tint operation** for images, so its color cannot be changed per page programmatically — only swapped via `update_fill` if a pre-colored logo asset exists. Leave the logo as-is unless a colored variant asset is provided.

### Page map (6 pages, 1080×1350)
| Page | Role | Key elements |
|---|---|---|
| 1 | Cover | kicker `WEEKLY TREND BRIEF · {YYYY.MM.DD}` · wordmark `Trend News` · 3-line headline · subtext · `밀어서 보기 →` · dark grid + logo |
| 2 | Trend #1 | kicker `#1 · {CATEGORY}` · title · body(3 lines)+reference block · photo background |
| 3 | Trend #2 | kicker `#2 · {CATEGORY}` · title · body+references · photo background |
| 4 | Trend #3 | kicker `#3 · {CATEGORY}` · title · body+references · photo background |
| 5 | Trend #4 | kicker `#4 · {CATEGORY}` · title · body+references · photo background |
| 6 | Summary | `SUMMARY · 이번 주의 문법` · 3-line keyword headline · 2-line recap · `다음 주에 또 만나요 👋` |

### Reference block format (bottom of pages 2–5, inside the body text element)
Append to the body text, after the 3 content lines:
```
{3 body lines}

──────────────
참고 ·  {매체} 「{기사 제목}」 {YYYY.MM.DD}
·  {매체2} 「{기사 제목2}」 {YYYY.MM.DD}
```
- Use 1–2 sources per page from ROLE_2 references.
- `──────────────` is a literal divider line (14 box-drawing chars).
- Keep outlet/article names as published (English allowed for foreign outlets).

---

## Step 1 — Copy the master

`copy-design` with `design_id: DAHLSzY4WsQ`, title `Trend News · {YYYY.MM.DD}`.
Record the new `design_id` and its edit URL.

## Step 2 — Upload this week's 4 background photos

For each trend's ROLE_3 card image URL, call `upload-asset-from-url` → record the 4 returned `asset_id`s.
(These replace the previous week's backgrounds on pages 2–5.)

## Step 3 — Open an editing transaction

`start-editing-transaction` on the new copy's `design_id`.
The response returns **all `richtexts` and `fills` with their current element IDs**. Element IDs are unique per design copy, so **map them by current text / page**, not by memorized IDs:
- Cover: kicker (`WEEKLY TREND BRIEF · …`), wordmark (`Trend News`), headline, subtext.
- Pages 2–5: kicker (`#N · …`), title, body, and the full-page photo `fill` element.
- Page 6: summary kicker, headline, recap, button.

## Step 4 — Replace all content (batch into one `perform-editing-operations` call where possible)

Use these operation types only (Canva cannot create new elements):
- `replace_text` — cover date+headline, each page's kicker/title/body(+reference block), summary text.
- `update_fill` — swap each page 2–5 background photo element to this week's uploaded `asset_id`.
- `format_text` — only if a contrast fix is needed (see Step 5).

**Text color rule (verified readable):**
- Content pages (2–5) use a **light page base + photo texture + DARK text**: title `#11121A`, body `#1E2230`, kicker `#2E6FB0`.
- Cover + summary sit on the **dark grid**, so their text stays **light** (white / blue) — leave as-is from the master.

**Background opacity rule:** photos sit at ~`0.26–0.42` opacity over the light base so dark text stays legible. If a swapped photo is dark/busy, lower its opacity toward `0.26`.

## Step 5 — Verify readability (mandatory, mid-transaction)

`get-design-thumbnail` for content pages **2–5 only** (cover/summary are text-only and unchanged in layout; `start-editing-transaction` already returns the cover thumbnail). Check:
- No text clipped or overflowing the card.
- Dark text is clearly legible over the photo (no washout, no dark-on-dark).
- Reference block fits in the lower area and looks balanced.

If a page fails: lower that photo's opacity (re-`update_fill` / re-insert at lower opacity) or shorten the flagged text, then re-fetch **only that page**. Don't commit until pages 2–5 pass.

## Step 6 — Commit

`commit-editing-transaction` on the transaction. Autonomously — do **not** ask the user first (global constraint). Record the final edit link from `get-design`.

---

## Step 7 — Write the Instagram caption

Write `output/post_{MMDD}.txt`.

### Format
```
[한두 줄 훅 — 이번 주 트렌드를 한 문장으로]

——

01 · [카테고리]
[2–3문장 요약. 자연스러운 구어체, ~해요 / ~이에요 톤]

02 · [카테고리]
[2–3문장]

03 · [카테고리]
[2–3문장]

04 · [카테고리]
[2–3문장]

——

[마무리 한 줄 — 구독/참여 유도]

#트렌드레터 #GenZLab #TrendNews #2026트렌드
#[카테고리태그1] #[카테고리태그2] #[카테고리태그3] #[카테고리태그4]
```

### Tone rules
- 사람이 직접 쓴 것처럼 자연스럽게, 각 트렌드 2–3문장
- 해시태그 8–10개, 마지막 줄에 모아서

---

## Step 8 — Send the single Telegram completion message

Send **one** Telegram reply. Attach the 2 files (`files` array) and put the Canva link in the message body.

```
✅ 이번 주 트렌드 레터 완성됐어요! ({YYYY.MM.DD})

📄 HTML 뉴스레터 + 📝 인스타 캡션 첨부했어요.
🎨 Trend News 카드뉴스(캔바): {canva_edit_link}

📌 이번 호 4가지 트렌드:
1. [이모지] [trend title 1]
2. [이모지] [trend title 2]
3. [이모지] [trend title 3]
4. [이모지] [trend title 4]

🖼 이미지 소스: [domain1] + [domain2] + [domain3]
```

Attach (absolute paths, confirm both exist on disk first):
```
files: [
  "output/trend_letter_{MMDD}.html",
  "output/post_{MMDD}.txt"
]
```

---

## Content Limits (prevent card overflow)
- Cover headline: 3 short lines, each ≤ 8 Korean chars
- Page 2–5 title: ≤ 12 Korean chars
- Page 2–5 body: 3 lines, each ≤ 30 Korean chars
- Reference block: ≤ 2 sources, each line ≤ 40 chars
- Summary headline: 3 lines, each ≤ 8 chars

## Failure Handling
- `copy-design` / `upload-asset-from-url` failure → retry once, then send Telegram error naming the step.
- Uncommitted transaction must never be left open — either commit (on success) or `cancel-editing-transaction` (on abort).
