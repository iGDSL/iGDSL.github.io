#!/usr/bin/env python3
"""
iGDSL 홈페이지 — 연구 키워드 워드클라우드 이미지 생성 (선택 사항)

*** 홈페이지에는 필요 없습니다. ***
논문 페이지의 키워드 구름은 브라우저가 그 자리에서 그리므로 이 스크립트를
돌리지 않아도 논문만 추가하면 저절로 갱신됩니다.

이 스크립트는 발표자료·포스터에 넣을 그림 파일(images/keywords.png)이
필요할 때만 씁니다. 홈페이지와 똑같이 assets/keywords-data.js 의 키워드
표와 assets/pubs-data.js 의 논문 제목을 읽어 만듭니다.

    pip install wordcloud
    python3 tools/keywords.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBS = ROOT / "assets" / "pubs-data.js"
KWJS = ROOT / "assets" / "keywords-data.js"      # 홈페이지와 공유하는 키워드 표
OUT_PNG = ROOT / "images" / "keywords.png"
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"   # 없으면 아래에서 대체

def load_keywords():
    """assets/keywords-data.js 의 KEYWORDS 표를 읽어옵니다.
    홈페이지와 같은 파일을 쓰므로 두 곳이 어긋날 일이 없습니다."""
    if not KWJS.exists():
        sys.exit(f"찾을 수 없음: {KWJS}")
    text = KWJS.read_text(encoding="utf-8")
    m = re.search(r"const\s+KEYWORDS\s*=\s*\{(.*?)\n\};", text, re.S)
    if not m:
        sys.exit("keywords-data.js 에서 KEYWORDS 표를 찾지 못했습니다.")
    out = {}
    for line in m.group(1).splitlines():
        line = line.split("//")[0].strip()
        e = re.match(r"""['"](.+?)['"]\s*:\s*\[(.*?)\]\s*,?$""", line)
        if e:
            pats = re.findall(r"""['"](.+?)['"]""", e.group(2))
            if pats:
                out[e.group(1)] = pats
    if not out:
        sys.exit("KEYWORDS 표가 비어 있습니다.")
    return out


# 빈도가 높을수록 진한 남색 (브랜드 색)
SHADES = ['#003354', '#004d82', '#1b6596', '#3a7ba8', '#6098bd', '#8fb6d0']


def find_font():
    import matplotlib.font_manager as fm
    if Path(FONT).exists():
        return FONT
    for want in ('Poppins', 'DejaVu Sans', 'Arial', 'Helvetica'):
        try:
            p = fm.findfont(fm.FontProperties(family=want, weight='bold'), fallback_to_default=False)
            if p and Path(p).exists():
                return p
        except Exception:
            pass
    return fm.findfont(fm.FontProperties(weight='bold'))


def main():
    if not PUBS.exists():
        sys.exit(f"찾을 수 없음: {PUBS}")

    titles = [t.lower() for t in re.findall(r"title:\s*'([^']+)'", PUBS.read_text(encoding='utf-8'))]
    if not titles:
        sys.exit("pubs-data.js 에서 논문 제목을 찾지 못했습니다.")

    keywords = load_keywords()
    freq = {}
    for label, pats in keywords.items():
        n = sum(1 for t in titles if any(p in t for p in pats))
        if n:
            freq[label] = n

    print(f"논문 {len(titles)}편에서 키워드 {len(freq)}개\n")
    for k, v in sorted(freq.items(), key=lambda x: -x[1]):
        print(f"  {v:3d}편  {k}")

    try:
        from wordcloud import WordCloud
    except ImportError:
        sys.exit("\nwordcloud 가 없습니다.  pip install wordcloud  후 다시 실행하세요.")

    mx = max(freq.values())

    def color(word, **kw):
        r = freq.get(word, 1) / mx
        return SHADES[min(len(SHADES) - 1, int((1 - r) * len(SHADES)))]

    wc = WordCloud(
        width=1600, height=620,
        background_color=None, mode='RGBA',
        font_path=find_font(),
        prefer_horizontal=0.92,
        max_font_size=150, min_font_size=15,
        relative_scaling=0.55,
        margin=8,
        random_state=7,          # 같은 배치를 유지하려면 이 값을 고정
        color_func=color,
    ).generate_from_frequencies(freq)

    wc.to_file(str(OUT_PNG))

    print(f"\n저장: {OUT_PNG.relative_to(ROOT)}  (발표자료용)")


if __name__ == "__main__":
    main()
