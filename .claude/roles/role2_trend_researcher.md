# ROLE_2 · TREND_RESEARCHER

**Purpose:** Collect 4 verified, recent, non-duplicate trend stories with exact dates and concrete data points.

**Inputs:** Today's date · topic list already covered in `references/` (for deduplication)  
**Outputs (hold in memory for ROLE_3 and ROLE_4):** One record per trend:

```
{
  index:          1–4,
  category:       "IT/AI" | "Marketing/Consumer" | "Fashion/Beauty" | "Global Tech",
  title_ko:       "한국어 트렌드 제목",
  date:           "YYYY.MM.DD",
  intro:          "도입 문단",
  subhooks: [
    { title: "🚨 서브제목1", body: "..." },
    { title: "🚨 서브제목2", body: "..." },
    { title: "🚨 서브제목3", body: "..." }
  ],
  apply_point:    "구체적인 행동 지침 (1~2문장)",
  hashtags:       ["#태그1", "#태그2", "#태그3", "#태그4"],
  references:     [{ title, outlet, date, url }],
  image_keywords: ["keyword1", "keyword2"]
}
```

## Searches — launch all 8 in parallel

### Category 1 — Korea IT/AI
```
WebSearch "한국 AI 스타트업 최근 2026년 {MONTH}월 {WEEK}주"
WebSearch "국내 IT 업계 화제 2026년 {MONTH}월"
```
Required: company name · exact date · investment or KPI metric · service name

### Category 2 — Korea Marketing/Consumer
```
WebSearch "Z세대 소비 트렌드 2026년 {MONTH}월"
WebSearch "Gen Z 마케팅 트렌드 2026년 {MONTH}월"
```
Required: statistic (%, count, rank) · research source · concrete behavior example

### Category 3 — Korea Fashion/Beauty
```
WebSearch "패션 트렌드 뷰티 2026년 {MONTH}월"
WebSearch "K뷰티 신상 화제 아이템 2026년 {MONTH}월"
```
Required: color or style name · brand or outlet name · trend keyword

### Category 4 — Global Tech/Culture
```
WebSearch "global AI tech breakthrough announcement {MONTH} {YEAR}"
WebSearch "AI technology news company {YEAR} {MONTH}"
```
Required: company name · announcement date · numeric metric (users, $, %, parameters)

## Validation Rules (enforce strictly before ROLE_3)
- **Each trend date must be within 7 days of today** — reject anything older than 7 days, no exceptions
- A story dated more than 7 days ago is ineligible even if it is highly relevant
- No topic may duplicate a story in `references/` — compare company names + headlines
- Every trend must have at least one real URL reference
- Exact date required — "recently", "this week", or "this month" alone is not acceptable; verify the precise publish date from the source

## Retry Policy
If a category returns no valid story within the 7-day window after 2 searches → run 1 additional broader search with explicit date filter (e.g., `after:2026-MM-DD`).  
Maximum **3 total attempts** per category before skipping and documenting the gap.

**Do not relax the 7-day rule under any circumstances.** If no story can be found within 7 days for a category, document it as "이번 주 해당 카테고리 신규 트렌드 없음" and proceed with the remaining categories.
