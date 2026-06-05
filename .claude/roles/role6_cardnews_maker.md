# ROLE_6 · CARDNEWS_MAKER (Canva-native)

**Purpose:** Build the **"Trend News"** 7-page card news **inside Canva** by copying the approved master design and replacing its content, then write the Instagram caption and send the single Telegram completion message.

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

**Master design ID:** `DAHLrfLVQck` (Instagram portrait **1080×1350**, **7 pages**, wordmark "Trend News", dark editorial grid, blue accents, genZ lab logo top-right on every page).
Edit link: `https://www.canva.com/design/DAHLrfLVQck/edit`. This is the user's **finalized reference design** — the look the weekly output must match. Always **copy** this master — never edit the master itself. The copy inherits the exact layout, fonts, grid background, logo, reference-block styling, and the **finalized page order (Galaxy is page 6, Summary is page 7)**.
(Previous masters `DAHLTLAKV50` and `DAHLSzY4WsQ` are superseded by this reference.)

> Logo note: the genZ lab logo (asset `MAHLR2vMuLE`) is a **raster image** top-right on all 7 pages. The editing API exposes **no background-removal, filter/effect, or recolor/tint** operations for images — only replace (`update_fill`), move, resize, delete. So per-page logo recoloring (e.g. background-remove → color filter to match each page) is a **Canva-UI-only manual step**; the bot **leaves the logo untouched**. To enable programmatic per-page swaps instead, provide pre-colored logo asset IDs and the bot can `update_fill` each page.

### Page map (7 pages, 1080×1350)
| Page | Role | Key elements |
|---|---|---|
| 1 | Cover | kicker `WEEKLY TREND BRIEF · {YYYY.MM.DD}` · wordmark `Trend News` · 3-line weekly headline (각 행 ≤ 8자, 이번 주 분위기 압축) · subtext (3-line 4-trend summary) · `밀어서 보기 →` · dark grid + logo |
| 2 | Trend #1 | kicker `#1 · {CATEGORY}` · title · body(3 lines)+reference block · photo background |
| 3 | Trend #2 | kicker `#2 · {CATEGORY}` · title · body+references · photo background |
| 4 | Trend #3 | kicker `#3 · {CATEGORY}` · title · body+references · photo background |
| 5 | Trend #4 | kicker `#4 · {CATEGORY}` · title · body+references · photo background |
| 6 | Galaxy | kicker `FOR GALAXY` · title `갤럭시라면?` · 4-line apply block (① ② ③ ④ 형식, 각 트렌드→갤럭시 적용 질문) · 구분선+마무리 한 줄 · photo background |
| 7 | Summary | kicker `SUMMARY` · label+keyword block `이번 주의 키워드,\n[단어]` · 2-line recap · button `다음 주에 또 만나요 👋` |

**Page 6 (Galaxy) 작성 규칙:**
- kicker: 항상 `FOR GALAXY` (고정 — "직원" 등 내부용 표현 금지, 인스타그램 공개 게시용)
- title: 항상 `갤럭시라면?`
- body: 4가지 트렌드 각각에 대해 갤럭시 관점의 질문 한 줄 (① ② ③ ④), 구분선 후 행동 유도 한 줄
- 배경: 이번 주 미사용 Pexels 이미지 (스마트폰·기기·테크 테마 권장)

### Reference block format (bottom of pages 2–5, inside the body text element)
Append to the body text, after the 3 content lines:
```
{3 body lines}

─────────────────────
참고
·  {매체} 「{기사 제목}」 {YYYY.MM.DD}
·  {매체2} 「{기사 제목2}」 {YYYY.MM.DD}
```
- Use 1–2 sources per page from ROLE_2 references.
- `─────────────────────` is a literal divider line (21 box-drawing chars).
- **`참고` sits on its own line; each source line starts with `·` on a new line** (참고 뒤에 줄바꿈, 각 출처는 별도 줄).
- Keep outlet/article names as published (English allowed for foreign outlets).

---

## Step 1 — Copy the master

`copy-design` with `design_id: DAHLrfLVQck`.
Record the new `design_id` and its edit URL. The copy already has **all 7 pages** including the Galaxy page (page 6) — no page needs to be created or appended.

> ⚠️ `copy-design` has **no title parameter**, so the copy inherits the master's name. You **must** rename it in Step 4 via an `update_title` operation → `Trend News · {YYYY.MM.DD}` (브랜드 통일감).

## Step 2 — Upload this week's 5 background photos

Call `upload-asset-from-url` for each and record the returned `asset_id`s:
- **4 trend card images** (ROLE_3) → replace backgrounds on pages 2–5.
- **1 Galaxy page image** → replace background on page 6. Use an **unused** Pexels smartphone/device/tech image (check the No-Reuse list in ROLE_3).

## Step 3 — Open an editing transaction

`start-editing-transaction` on the new copy's `design_id`.
The response returns **all `richtexts` and `fills` with their current element IDs**. Element IDs are unique per design copy, so **map them by current text / page**, not by memorized IDs:
- Cover: kicker (`WEEKLY TREND BRIEF · …`), wordmark (`Trend News`), headline, subtext.
- Pages 2–5: kicker (`#N · …`), title, body, and the full-page photo `fill` element.
- Page 6 (Galaxy): kicker (`FOR GALAXY`), title (`갤럭시라면?`), body (① ② ③ ④ block), and the full-page photo `fill` element.
- Page 7 (Summary): summary kicker, keyword block, recap, button.

## Step 4 — Replace all content (batch into one `perform-editing-operations` call where possible)

Use these operation types only (Canva cannot create new elements):
- `update_title` — set the design title to `Trend News · {YYYY.MM.DD}` (브랜드 통일감 — never leave it as "Trend News Reference").
- `replace_text` — cover kicker (date only) + cover subtext (weekly summary); each trend page's kicker/title/body(+reference block); the Galaxy page (6) body (4 trend→Galaxy questions); summary text.
- `update_fill` — swap each page 2–6 background photo element to this week's uploaded `asset_id` (4 trends + 1 Galaxy).
- `format_text` — only if a contrast fix is needed (see Step 5).

**Cover FIXED elements — NEVER replace these:**
- Wordmark `Trend News` — always leave as-is.

**Text color rule (verified readable):**
- Content pages (2–6, trends + Galaxy) use a **light page base + photo texture + DARK text**: title `#11121A`, body `#1E2230`, kicker `#2E6FB0`.
- Cover + summary sit on the **dark grid**, so their text stays **light** (white / blue) — leave as-is from the master.

**Background opacity rule:** photos sit at ~`0.26–0.42` opacity over the light base so dark text stays legible. If a swapped photo is dark/busy, lower its opacity toward `0.26`.

## Step 5 — Verify readability (mandatory, mid-transaction)

`get-design-thumbnail` for content pages **2–6** (4 trends + Galaxy) and **page 7 (summary)**. Check:
- No text clipped or overflowing the card.
- Dark text is clearly legible over the photo (no washout, no dark-on-dark).
- Reference block (pages 2–5) and the Galaxy ① ② ③ ④ block (page 6) fit in the lower area and look balanced.
- **Page 7 specific:** confirm `이번 주의 키워드` label is visible as a single line (white text on dark background). If it is missing or invisible, re-apply `replace_text` to element with current text closest to that phrase.

If a page fails: lower that photo's opacity (re-`update_fill` / re-insert at lower opacity) or shorten the flagged text, then re-fetch **only that page**. Don't commit until pages 2–7 pass.

## Step 6 — Commit

`commit-editing-transaction` on the transaction. Autonomously — do **not** ask the user first (global constraint). Record the final edit link from `get-design`.

> Note: the Galaxy page (page 6) is **baked into the master** `DAHLrfLVQck`, so it is edited inline in Step 4 like any other page — there is **no copy/merge step** anymore. The committed design already has all 7 pages in the correct order.

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

### Append a background-music block to the caption file
At the bottom of `output/post_{MMDD}.txt`, after the hashtag line, append a `🎵 추천 배경음악` block so the recommendation ships with the caption (creator can pick it directly in the Instagram audio picker):
```

——

🎵 추천 배경음악 (인스타 오디오 검색용)
1. [트랙명 — 아티스트] · [무드]
2. [트랙명 — 아티스트] · [무드]
3. [트랙명 — 아티스트] · [무드]
```

---

## Step 7b — Recommend Instagram background music

The card news posts as a **carousel / Reel**, so pick audio that fits a Gen-Z editorial trend brief: **clean, modern, low-vocal, upbeat-but-calm** so on-screen Korean text stays the focus. Recommend **3 tracks**, each tagged with a mood, drawn from sources a creator can actually use inside the Instagram app.

**Selection rules**
- Prefer tracks **searchable in Instagram's in-app audio library** (`오디오 추가` picker) — that is the only audio a personal/creator account can attach to a Reel/carousel without licensing friction.
- Match the mood to the week's lead trend: AI/tech weeks → minimal electronic / future-funk; consumer/lifestyle → warm lo-fi / chillhop; fashion/beauty → dreamy synth-pop / soft house.
- Keep it **low-vocal or instrumental** so the headline text reads clearly; avoid lyric-heavy or high-energy drops that fight the copy.
- Note that licensed commercial pop may be **region/account-type restricted** — always offer at least one **royalty-free / Instagram-original** fallback.

**Default go-to pool (safe, Instagram-available moods)**
| Mood | Use when | Example direction |
|---|---|---|
| Minimal electronic / future-funk | AI · 글로벌 테크 주제 | clean four-on-the-floor, light synth pluck, no vocals |
| Warm lo-fi / chillhop | 소비·라이프스타일 주제 | mellow boom-bap, vinyl texture, cozy keys |
| Dreamy synth-pop / soft house | 패션·뷰티 주제 | airy pads, soft female hum, gentle groove |
| Trending Reels audio (이번 주 인기 오디오) | 도달·노출 우선일 때 | pick a currently-rising sound from the 인기 탭, low-vocal preferred |

Output the 3 picks (track name + artist where known + mood) into the caption file (above) **and** restate them in the Telegram completion message.

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

🎵 추천 배경음악 (인스타 오디오): [track 1] · [track 2] · [track 3]
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
- Summary keyword block: `이번 주의\n키워드,\n[단어]` — always **3 lines**: line 1 `이번 주의`, line 2 `키워드,` (with comma), line 3 is **one Korean word** (2–4 chars) that compresses all 4 trends (e.g. `도약`, `확산`, `전환`, `돌파`). Never omit the keyword word.

## Failure Handling
- `copy-design` / `upload-asset-from-url` failure → retry once, then send Telegram error naming the step.
- Uncommitted transaction must never be left open — either commit (on success) or `cancel-editing-transaction` (on abort).
