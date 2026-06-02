# ROLE_3 · IMAGE_SOURCER

**Purpose:** Source and verify 3 images per trend (1 card background + 2 inline body) from ≥3 distinct domains.

**Inputs:** `image_keywords` from each of the 4 trend records  
**Outputs (hold in memory for ROLE_4):**
```
trend_1: { card: "URL", inline_1: "URL", inline_2: "URL" },
trend_2: { card: "URL", inline_1: "URL", inline_2: "URL" },
trend_3: { card: "URL", inline_1: "URL", inline_2: "URL" },
trend_4: { card: "URL", inline_1: "URL", inline_2: "URL" }
```

## Supported Sources

### Pexels (most reliable for hotlinking)
```
WebFetch https://www.pexels.com/search/{keyword}/
```
Extract photo IDs → final URL:
```
https://images.pexels.com/photos/{ID}/pexels-photo-{ID}.jpeg?auto=compress&cs=tinysrgb&w=630
```

### Unsplash (lifestyle, tech, people)
```
WebFetch https://unsplash.com/s/photos/{keyword}
```
Then fetch the photo page to get the numeric CDN ID:
```
WebFetch https://unsplash.com/photos/{slug}
```
Final URL: `https://images.unsplash.com/photo-{numeric-id}?w=630&q=80`

### Wikimedia Commons (real-world subjects, always publicly licensed)
```
WebFetch https://commons.wikimedia.org/w/index.php?search={keyword}&ns6=1
```
Then get direct URL from file page:
```
WebFetch https://commons.wikimedia.org/wiki/File:{filename}
```
Final URL: `https://upload.wikimedia.org/wikipedia/commons/{path}/{filename}`

⚠️ Fetch one Wikimedia URL at a time — batch requests risk HTTP 429 rate limiting.

## Verification (mandatory for every candidate URL)

Batch-check where possible:
```bash
curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" -A "Mozilla/5.0" "URL1" "URL2" ...
```
- HTTP `200` → accepted
- HTTP `404` / `429` / other → discard, try next candidate from a different source
- Maximum **3 candidates per slot** before marking as failed

## No-Reuse Rule (mandatory)
**Never reuse a Pexels photo ID that appeared in any previous issue.**  
Known used IDs (cumulative — append each week's IDs after publishing):
```
# Vol.22 / 0601
8386437, 2599244, 8439093, 8199219, 6340704, 9630189, 7043582, 3762890,
12124831, 17489163, 6636463, 51165

# Vol.23 / 0602
8566526, 534216, 785418
```
Before picking a candidate: confirm its ID does **not** appear in the list above.  
If the first search returns only used IDs, run a second search with different keywords and pick a fresh ID.

## Domain Diversity Rule
After filling all 12 slots, count distinct top-level domains.  
**Minimum 3 distinct domains required.**  
If fewer than 3 covered → explicitly source remaining images from untapped domains before proceeding.

## Theme Guidance

| Category | Search Keywords |
|---|---|
| IT/AI | `artificial-intelligence`, `technology-chip`, `robot`, `computer-vision`, `data-center` |
| Marketing/Consumer | `convenience-store`, `young-people-shopping`, `grocery`, `lifestyle` |
| Fashion/Beauty | `fashion-runway`, `colorful-outfit`, `skincare`, `beauty-product` |
| Global Tech | `quantum-computer`, `smartphone`, `data-center`, `circuit-board` |

## Caption Format
Append source credit to every image caption:
- `/ Pexels`
- `/ Unsplash`
- `/ Wikimedia Commons`

## Failure Handling
If a slot cannot be filled after 3 attempts across all 3 sources → use any verified 200-returning image from the same thematic category.  
**Never embed an unverified URL in the final HTML.**
