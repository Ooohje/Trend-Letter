"""
Trend Snap HTML Generator
Usage: python generate_trendsnap.py path/to/trendsnap_data.json
Reads trendsnap_template.html from the same references/ dir and fills placeholders.
Outputs: output/cardnews/{MMDD}/trendsnap_{MMDD}.html
"""
import json, sys
from pathlib import Path

REF_DIR = Path(__file__).parent

def generate(json_path: str) -> str:
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    template = (REF_DIR / "trendsnap_template.html").read_text(encoding="utf-8")

    # ── Top-level tokens ──────────────────────────────────────────────────
    html = template
    html = html.replace("{{VOL}}",       data["vol"])
    html = html.replace("{{DATE_FULL}}", data["date_full"])
    html = html.replace("{{MMDD}}",      data["mmdd"])

    # ── Logo path (relative from output/cardnews/{MMDD}/ to project root) ─
    html = html.replace("{{LOGO_PATH}}", "../../../GenZ%20Lab._Logo.png")

    # ── Per-trend tokens (T1–T4) ──────────────────────────────────────────
    for i, t in enumerate(data["trends"], 1):
        prefix = f"T{i}"
        simple_keys = [
            "category", "lbl_class", "dot_class", "bg_url",
            "hl1", "hl2", "subline",
            "p1", "p2", "p3",
            "pull", "tags",
            "cover_cat", "cover_title",
            # Marketing-specific
            "big_stat", "stat_unit", "pill1", "pill2", "pill3", "note",
            # Fashion-specific
            "color1", "color2", "color3", "color4",
            # Tech-specific
            "big_num", "num_unit", "stat1", "stat2", "stat3",
            # Source credits (shown below stat in card)
            "stat_source",
        ]
        for key in simple_keys:
            placeholder = f"{{{{{prefix}_{key.upper()}}}}}"
            html = html.replace(placeholder, str(t.get(key, "")))

    # ── Outro tokens ──────────────────────────────────────────────────────
    for i, line in enumerate(data.get("poem_lines", []), 1):
        html = html.replace(f"{{{{POEM_L{i}}}}}", line)
    html = html.replace("{{POEM_L5}}", data.get("poem_l5", "이 시즌의 문법"))
    html = html.replace("{{CLOSING_NOTE}}", data.get("closing_note", "다음 Trend Snap도 함께해요 👋"))

    # ── Write output ──────────────────────────────────────────────────────
    out_dir = Path("output") / "cardnews" / data["mmdd"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"trendsnap_{data['mmdd']}.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"✓ HTML → {out_path}")
    return str(out_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_trendsnap.py <data.json>")
        sys.exit(1)
    generate(sys.argv[1])
