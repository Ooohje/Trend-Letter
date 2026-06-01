# ROLE_4 · CONTENT_WRITER

**Purpose:** Combine all role outputs into one complete, valid HTML newsletter file.

**Inputs:** CSS + class list (ROLE_1) · trend records (ROLE_2) · verified image URLs (ROLE_3)  
**Output:** Complete HTML string passed to ROLE_5 for writing to disk

## Document Structure (strict order)

```
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>[Korean newsletter title]</title>
  <style>[VERBATIM CSS FROM ROLE_1]</style>
</head>
<body>
<div class="outer">

  [1]  .meta                  "Trend Letter · {YYYY.MM.DD}"  (date, NOT a Vol number)
  [2]  cover div              dark background · {YYYY.MM.DD} · Korean date range
  [3]  .credits               date range notice (Korean)
  [4]  .divider-space
  [5]  .block.top             2–3 intro paragraphs (seasonal + timely, Korean)
  [6]  .section-title × 4    TOC: all 4 trend titles prefixed #1 #2 #3 #4
  [7]  .divider-space

  ── REPEAT × 4 (one block per trend) ────────────────────────────────────
  [A]  .trend-card            gradient + ROLE_3 card image background
  [B]  .block.top             intro paragraph (Korean)
  [C]  .inline-img > img      ROLE_3 inline_1 · Korean alt · caption
  [D]  .caption               "[description] / [Source]"
  [E]  .subhook               🚨 subhook title 1
  [F]  .block                 paragraph 1 (Korean)
  [G]  .inline-img > img      ROLE_3 inline_2 · Korean alt · caption
  [H]  .caption
  [I]  .subhook               🚨 subhook title 2
  [J]  .block                 paragraph 2 (Korean)
  [K]  .subhook               🚨 subhook title 3
  [L]  .block                 paragraph 3 (Korean)
  [M]  .apply-box             📌 적용 포인트 (concrete action, Korean)
  [N]  .hashtag-strip         HASHTAG + 4 tags
  [O]  .ref-label + .ref-item references with real anchor hrefs
  [P]  .divider-space
  ── END REPEAT ──────────────────────────────────────────────────────────

  [8]  .block.top.bottom      closing question paragraph (Korean)
  [9]  TrenderZ Station       .station-title + .station-sub + editor note
  [10] editor image placeholder
  [11] previous-issue link
  [12] .cta-wrap              feedback CTA button
  [13] .footer × 3           disclaimer · browser notice · {YYYY.MM.DD}  (date, no Vol)

</div>
</body>
</html>
```

## Card CSS Pattern (mandatory)
```css
.trend-card {
  background-image: linear-gradient(rgba(0,0,0,.45), rgba(0,0,0,.65)), url('{ROLE_3_card_url}');
  background-size: cover;
  background-position: center;
}
```

## Card Inner Content (all Korean)

| Element | Format |
|---|---|
| `.card-meta` | `#N · [CATEGORY] · KOREA · YYYY.MM.DD` |
| `.card-badge` | `KEYWORD·KEYWORD` (ALL CAPS, · separator) |
| `.card-headline` | Core sentence ≤ 20 Korean characters |
| `.card-tags` | `#태그1 &nbsp; #태그2 &nbsp; #태그3 &nbsp; #태그4` |

## Tone & Voice (strict)
- Style: `~해요`, `~인데요`, `~거든요`, `~이에요` — no 반말, ever
- Sentence length: max 2 lines per sentence
- Quotes: ≤15 words — prefer paraphrase over direct quote
- Emojis: only in `🚨` subhook labels and `📌` apply-box label — never in body prose
- Closing paragraph: must end with a question form  
  (예: `여러분은 ○○ 어떻게 느껴지시나요?`)

## Inline Stat Linking (mandatory)
When a specific statistic appears in body text and its source URL is known from ROLE_2 references, wrap the number with an anchor:
```html
<a href="[source_url]" target="_blank" style="color:inherit;text-decoration:underline;">34.1%</a>
```
Apply to: percentages, counts, rankings, named metrics — any figure traceable to a specific article URL.

## Pre-ROLE_5 Self-Check (run through every item before passing HTML to ROLE_5)

- [ ] 4 trends · each with exact date within 7 days of today
- [ ] 4 `.trend-card` blocks · each with verified CDN background + gradient overlay
- [ ] Each card: `.card-meta` + `.card-badge` + `.card-headline` + `.card-tags` (4 hashtags)
- [ ] Each trend: `inline_1` img + `inline_2` img · both from ROLE_3 verified list
- [ ] Every `<img>`: Korean `alt` attribute + `.caption` with domain credit
- [ ] Image domains: ≥3 distinct domains across all images
- [ ] Zero placeholder `<div>` for images — real `<img>` tags with verified CDN URLs only
- [ ] CSS is verbatim from ROLE_1 (no new rules added, none removed)
- [ ] `~해요` tone consistent throughout all body text
- [ ] All reference `href` values are real, non-placeholder URLs
- [ ] `📌` apply points are concrete, actionable Korean sentences
- [ ] No English visible in rendered output (CSS class names excepted)
