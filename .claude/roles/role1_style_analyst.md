# ROLE_1 · STYLE_ANALYST

**Purpose:** Extract exact CSS and structural patterns from reference files so every output matches brand style 100%.

**Inputs:** All files under `references/`  
**Outputs (hold in memory for ROLE_4):**
- Full `<style>` block to embed verbatim in the output HTML
- Confirmed CSS class names: `.trend-card`, `.card-meta`, `.card-badge`, `.card-headline`, `.card-tags`, `.block`, `.inline-img`, `.caption`, `.subhook`, `.apply-box`, `.hashtag-strip`, `.ref-label`, `.ref-item`, `.divider-space`, `.section-title`
- Confirmed tone markers: `~해요`, `~인데요`, `~거든요`, `~이에요`
- Section pattern: intro → 🚨 subhooks → 📌 apply-box → hashtag-strip → references

**Process:**
1. `Glob references/*.html` — list all reference files
2. Read `references/trend_letter_vol21.html` in full (primary quality benchmark)
3. For any file exceeding the read limit: use `Grep` to extract the `<style>` block and key structural class patterns
4. Confirm every CSS class listed in Outputs above is present — note any that are missing

**Acceptance gate:** CSS class list confirmed + tone style confirmed.  
If zero reference files are readable → halt all execution and report the error, stop.
