# ROLE_6 · CARDNEWS_MAKER

**Purpose:** Generate Trend Snap card news (6 PNG images + post.txt) from this week's trend data and send the Telegram completion message.

**Inputs:** Trend records from ROLE_2 memory · verified image URLs from ROLE_3 memory · `{MMDD}` and `{VOL}` from today's date  
**Outputs:** `output/cardnews/{MMDD}/trendsnap_{MMDD}.html` + 6 PNG files + `post.txt` + Telegram message

---

## Step 1 — Construct JSON Data File

Write `output/cardnews/{MMDD}/trendsnap_data.json` using ROLE_2 and ROLE_3 outputs.

### JSON Schema
```json
{
  "vol": "NN",
  "date_full": "YYYY.MM.DD",
  "mmdd": "MMDD",
  "trends": [
    {
      "index": 1,
      "category": "IT · AI · Korea · YYYY.MM",
      "lbl_class": "lbl-ai",
      "dot_class": "dot-ai",
      "bg_url": "ROLE_3 card image URL for trend 1",
      "hl1": "헤드라인 첫 번째 줄",
      "hl2": "헤드라인 두 번째 줄",
      "subline": "부제목 / 출처",
      "p1": "bullet 1 (HTML <strong> allowed)",
      "p2": "bullet 2 (HTML <strong> allowed)",
      "p3": "bullet 3 (HTML <strong> allowed)",
      "pull": "pull quote text",
      "tags": "#태그1 &nbsp; #태그2 &nbsp; #태그3 &nbsp; #태그4",
      "cover_cat": "IT · AI",
      "cover_title": "커버에 표시할 짧은 제목 (≤20자)"
    },
    {
      "index": 2,
      "category": "Marketing · Consumer · YYYY.MM",
      "lbl_class": "lbl-nano",
      "dot_class": "dot-nano",
      "bg_url": "ROLE_3 card image URL for trend 2",
      "hl1": "헤드라인 첫 번째 줄",
      "hl2": "헤드라인 두 번째 줄",
      "big_stat": "34.1%",
      "stat_unit": "Z세대 관련 통계 설명",
      "stat_source": "출처 · [리서치명], YYYY.MM",
      "pill1": "키워드1",
      "pill2": "키워드2",
      "pill3": "키워드3",
      "note": "한 줄 요약 (HTML <strong> allowed, <br> for line break)",
      "tags": "#태그1 &nbsp; #태그2 &nbsp; #태그3 &nbsp; #태그4",
      "cover_cat": "Marketing",
      "cover_title": "커버에 표시할 짧은 제목"
    },
    {
      "index": 3,
      "category": "Fashion · Beauty · YYYY S/S",
      "lbl_class": "lbl-style",
      "dot_class": "dot-style",
      "bg_url": "ROLE_3 card image URL for trend 3",
      "hl1": "헤드라인 첫 번째 줄",
      "hl2": "헤드라인 두 번째 줄",
      "color1": "RED",
      "color2": "BLUE",
      "color3": "GREEN",
      "color4": "YELLOW",
      "p1": "스타일 포인트 1 (HTML <strong> allowed)",
      "p2": "스타일 포인트 2",
      "p3": "스타일 포인트 3",
      "tags": "#태그1 &nbsp; #태그2 &nbsp; #태그3 &nbsp; #태그4",
      "cover_cat": "Fashion · Beauty",
      "cover_title": "커버에 표시할 짧은 제목"
    },
    {
      "index": 4,
      "category": "Global Tech · YYYY.MM.DD",
      "lbl_class": "lbl-tech",
      "dot_class": "dot-tech",
      "bg_url": "ROLE_3 card image URL for trend 4",
      "hl1": "헤드라인 첫 번째 줄",
      "hl2": "헤드라인 두 번째 줄",
      "big_num": "180",
      "num_unit": "QUBIT",
      "stat_source": "출처 · [매체명], YYYY.MM.DD",
      "stat1": "stat 1 (HTML <strong> allowed)",
      "stat2": "stat 2",
      "stat3": "stat 3",
      "tags": "#태그1 &nbsp; #태그2 &nbsp; #태그3 &nbsp; #태그4",
      "cover_cat": "Global Tech",
      "cover_title": "커버에 표시할 짧은 제목"
    }
  ],
  "poem_lines": [
    "트렌드1 핵심 한 줄,",
    "트렌드2 핵심 한 줄,",
    "트렌드3 핵심 한 줄,",
    "트렌드4 핵심 한 줄."
  ],
  "poem_l5": "이번 주의 문법을 요약하는 짧은 문장",
  "closing_note": "다음 Trend Snap도 함께해요 👋"
}
```

### Field Rules
- `hl1` + `hl2`: split headline at natural break, each ≤ 16 Korean characters
- `cover_title`: same as `hl1 + hl2` joined, ≤ 22 Korean characters total
- `big_stat` (T2): include % or ₩ symbol in the value string
- `stat_source` (T2, T4): `"출처 · [리서치/매체명], YYYY.MM"` — required when the stat has a verifiable source
- `color1–4` (T3): actual trend color names — can be Korean or English (e.g., "RED", "버건디")
- `big_num` (T4): numeric only, no unit (unit goes in `num_unit`)
- `tags`: use `&nbsp;` as separator, include the `#` prefix in each tag
- HTML in `p1/p2/p3`, `note`, `stat1/2/3`: only `<strong>` and `<br>` are allowed

---

## Step 2 — Generate HTML

```bash
python references/generate_trendsnap.py output/cardnews/{MMDD}/trendsnap_data.json
```

This writes `output/cardnews/{MMDD}/trendsnap_{MMDD}.html`.

---

## Step 3 — Generate PNG Images

```bash
python references/make_cardnews_images.py output/cardnews/{MMDD}/trendsnap_{MMDD}.html
```

The script:
1. Downloads all background image URLs and embeds as base64 data URIs (guarantees Chrome renders them without network)
2. Screenshots each card at 1080×1080 via Chrome Headless
3. Runs Pillow validation: background brightness check + overflow check

Output files in `output/cardnews/{MMDD}/`:
- `01_cover.png`, `02_ai.png`, `03_marketing.png`, `04_fashion.png`, `05_tech.png`, `06_outro.png`

### On ⚠️ warnings
- `배경 이미지 미로드` → the bg_url could not be downloaded. Replace the URL in the JSON and re-run Step 2+3.
- `텍스트 잘림 의심` → shorten the flagged field values in the JSON and re-run Step 2+3.

---

## Step 4 — Generate post.txt

Write `output/cardnews/{MMDD}/post.txt` — Instagram caption for the carousel post.

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
링크 인 바이오 📎

#트렌드레터 #GenZLab #TrendLetter #2026트렌드
#[카테고리태그1] #[카테고리태그2] #[카테고리태그3] #[카테고리태그4]
```

### Tone rules
- 사람이 직접 쓴 것처럼 자연스럽게
- 각 트렌드 2–3문장, 짧고 임팩트 있게
- 해시태그는 8–10개, 마지막 줄에 모아서

---

## Step 5 — Send Telegram Completion Message

Send **one** Telegram reply with all 8 files attached using the `files` array.

Message format:
```
✅ 트렌드 레터 Vol.NN + Trend Snap 완성됐어요!

📁 HTML 뉴스레터 + 카드뉴스 6장 + 인스타 캡션 첨부했어요.

📌 이번 호 4가지 트렌드:
1. [이모지] [trend title 1]
2. [이모지] [trend title 2]
3. [이모지] [trend title 3]
4. [이모지] [trend title 4]

🖼 이미지 소스: [domain1] + [domain2] + [domain3]
```

Attach all 8 files using their full absolute paths:
```
files: [
  "output/trend_letter_{MMDD}.html",
  "output/cardnews/{MMDD}/01_cover.png",
  "output/cardnews/{MMDD}/02_ai.png",
  "output/cardnews/{MMDD}/03_marketing.png",
  "output/cardnews/{MMDD}/04_fashion.png",
  "output/cardnews/{MMDD}/05_tech.png",
  "output/cardnews/{MMDD}/06_outro.png",
  "output/cardnews/{MMDD}/post.txt"
]
```

**Important:** Use absolute file paths resolved from the project working directory. All 8 files must be confirmed to exist on disk before calling reply.

## Content Limits (to prevent card overflow)
- `hl1` + `hl2` combined: ≤ 30 Korean characters
- `subline`: ≤ 25 characters
- `p1/p2/p3` each: ≤ 35 characters (including HTML tags)
- `pull`: ≤ 45 characters
- `stat_unit` (T2): ≤ 22 characters
- `stat_source` (T2, T4): ≤ 25 characters
- `note` (T2): ≤ 50 characters
- `stat1/2/3` (T4): ≤ 38 characters each
