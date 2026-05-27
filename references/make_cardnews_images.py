"""
Trend Snap 카드뉴스 → PNG 이미지 자동 생성 (재사용 가능 버전)
Usage: python make_cardnews_images.py path/to/trendsnap_{MMDD}.html

배경 이미지를 base64 data URI로 임베드한 뒤 Chrome Headless로 스크린샷.
(file:// 또는 http:// 프로토콜 모두 외부 CSS background-image 로딩 불안정 →
 data URI 임베드로 100% 로딩 보장)

검증:
  - 사전: HTML의 모든 background-image URL HTTP 200 확인
  - 임베드: 검증 통과 URL을 data URI로 치환 → 네트워크 없이 렌더링
  - 사후(Pillow 설치 시):
      · 배경 밝기 체크 (배경 미로드 감지, 임베드 실패 보험)
      · 하단 잘림 체크 (텍스트 overflow 감지)
"""
import base64
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

PHOTO_CARDS = {"c1", "c2", "c3", "c4"}   # 배경 사진이 있어야 하는 카드

CARDS = [
    ("01_cover",     "c0"),
    ("02_ai",        "c1"),
    ("03_marketing", "c2"),
    ("04_fashion",   "c3"),
    ("05_tech",      "c4"),
    ("06_outro",     "c5"),
]


# ── URL 검증 및 data URI 임베드 ───────────────────────────────────────────────

def _fetch(url: str) -> bytes | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        return urllib.request.urlopen(req, timeout=15).read()
    except Exception:
        return None


def verify_and_embed(html: str) -> tuple[str, list[str]]:
    """
    HTML 안의 모든 CSS url(https://...) 을 base64 data URI로 교체.
    반환: (수정된 HTML, 실패한 URL 목록)
    """
    urls = list(dict.fromkeys(
        re.findall(r"url\(['\"]?(https?://[^'\")]+)['\"]?\)", html)
    ))
    failed = []

    for url in urls:
        data = _fetch(url)
        if data is None:
            failed.append(url)
            continue

        ext = url.split("?")[0].lower()
        if   ext.endswith(".png"):  mime = "image/png"
        elif ext.endswith(".webp"): mime = "image/webp"
        else:                       mime = "image/jpeg"

        data_uri = f"data:{mime};base64,{base64.b64encode(data).decode()}"
        for q in ("'", '"', ""):
            html = html.replace(f"url({q}{url}{q})", f"url('{data_uri}')")

    return html, failed


# ── 단일 카드 HTML ────────────────────────────────────────────────────────────

def make_single_card_html(embedded_html: str, card_id: str) -> str:
    override = f"""
<style id="__ss">
  body {{ padding: 0 !important; background: #0e0e0e !important; overflow: hidden !important; }}
  .guide {{ display: none !important; }}
  .card {{ display: none !important; margin: 0 !important; }}
  #{card_id} {{ display: flex !important; margin: 0 !important; }}
</style>"""
    return embedded_html.replace("</head>", override + "\n</head>")


# ── 사후 검증 (Pillow) ───────────────────────────────────────────────────────

def _pillow_checks(out: Path, cid: str, tmp: Path) -> list[str]:
    try:
        from PIL import Image
    except ImportError:
        return []

    warnings = []
    img = Image.open(out)

    # 1) 배경 이미지 로드 실패 감지
    if cid in PHOTO_CARDS:
        top = img.crop((0, 0, 1080, 300))
        pixels = list(top.getdata())
        avg_brightness = sum(max(p[:3]) for p in pixels) / len(pixels)
        if avg_brightness < 30:
            warnings.append(
                f"배경 이미지 미로드 의심 (상단 평균 밝기 {avg_brightness:.0f}/255)"
            )

    # 2) overflow 감지 — 1080×1120 스크린샷, 하단 40px 확인
    chk = tmp.parent / f"_ovf_{cid}.png"
    file_url = "file:///" + str(tmp).replace("\\", "/").replace(" ", "%20")
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--disable-extensions", "--force-device-scale-factor=1",
         "--hide-scrollbars", "--run-all-compositor-stages-before-draw",
         "--window-size=1080,1120", f"--screenshot={chk}", file_url],
        capture_output=True, timeout=30,
    )
    if chk.exists():
        try:
            chk_img = Image.open(chk)
            strip = chk_img.crop((0, 1080, 1080, min(chk_img.height, 1120)))
            non_bg = sum(1 for p in strip.getdata() if max(p[:3]) > 40)
            if non_bg > 300:
                warnings.append(f"텍스트 잘림 의심 (하단 {non_bg}px 초과)")
        except Exception:
            pass
        finally:
            chk.unlink(missing_ok=True)

    return warnings


# ── 메인 ─────────────────────────────────────────────────────────────────────

def generate(html_file: str) -> None:
    html_path = Path(html_file).resolve()
    if not html_path.exists():
        print(f"✗ HTML 파일을 찾을 수 없어요: {html_path}")
        sys.exit(1)

    base = html_path.parent
    source = html_path.read_text(encoding="utf-8")
    mmdd = html_path.stem.replace("trendsnap_", "")

    print(f"\n▶ Trend Snap {mmdd} 카드뉴스 이미지 생성\n")

    # ── 배경 이미지 임베드 ────────────────────────────────────────────────────
    bg_urls = list(dict.fromkeys(
        re.findall(r"url\(['\"]?(https?://[^'\")]+)['\"]?\)", source)
    ))
    if bg_urls:
        print(f"  🔗 배경 이미지 {len(bg_urls)}개 다운로드 및 임베드 중...")
        source, failed = verify_and_embed(source)
        if failed:
            for u in failed:
                print(f"  ⚠️  다운로드 실패: {u[:80]}")
            print(f"  → 위 이미지는 배경에 표시되지 않아요. JSON 수정 후 재생성 권장.")
        else:
            print(f"  ✓  모든 배경 이미지 임베드 완료")
    print()
    print(f"  출력 위치: {base}\n")

    ok, fail = 0, 0

    for name, cid in CARDS:
        tmp = base / f"_tmp_{cid}.html"
        out = base / f"{name}.png"

        tmp.write_text(make_single_card_html(source, cid), encoding="utf-8")
        file_url = "file:///" + str(tmp).replace("\\", "/").replace(" ", "%20")

        result = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
             "--disable-extensions", "--force-device-scale-factor=1",
             "--hide-scrollbars", "--run-all-compositor-stages-before-draw",
             "--window-size=1080,1080", f"--screenshot={out}", file_url],
            capture_output=True, timeout=30,
        )

        if out.exists() and out.stat().st_size > 10_000:
            kb = out.stat().st_size // 1024
            warns = _pillow_checks(out, cid, tmp)
            tmp.unlink(missing_ok=True)

            if warns:
                print(f"  ⚠️  {name}.png  ({kb} KB) — {' / '.join(warns)}")
            else:
                print(f"  ✓  {name}.png  ({kb} KB)")
            ok += 1
        else:
            tmp.unlink(missing_ok=True)
            print(f"  ✗  {name}.png  — 생성 실패")
            if result.stderr:
                print(f"     {result.stderr.decode(errors='ignore')[:120]}")
            fail += 1

    print(f"\n  완료: {ok}장 성공 / {fail}장 실패")
    if fail > 0:
        print(f"  ※ 실패한 카드가 있어요. JSON 데이터와 URL을 확인해주세요.")
    print(f"  폴더: {base}\n")

    if fail > 0:
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python make_cardnews_images.py <trendsnap_MMDD.html>")
        sys.exit(1)
    generate(sys.argv[1])
