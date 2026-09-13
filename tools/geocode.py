#!/usr/bin/env python3
"""
iGDSL 홈페이지 — 장소 이름 지오코딩 스크립트

gallery/gallery-data.js 에 적힌 place 이름을 읽어,
아직 gallery/places.js 에 좌표가 없는 것만 OpenStreetMap Nominatim 으로
찾아서 places.js 에 추가합니다.

사용법 (홈페이지 폴더에서):

    python3 tools/geocode.py              # 새 장소만 찾기
    python3 tools/geocode.py --force      # 전부 다시 찾기
    python3 tools/geocode.py --dry-run    # 결과만 보고 파일은 건드리지 않기

Nominatim 이용정책상 초당 1회로 제한하고 연락처를 User-Agent 에 담아 보냅니다.
찾은 좌표는 places.js 에 저장되므로, 홈페이지를 열 때는 외부 호출이 없습니다.

주의: 지오코딩 결과가 늘 정확하진 않습니다. 실행 후 places.js 를 열어
      좌표를 확인하고, 필요하면 직접 고쳐 주세요.
"""

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "gallery" / "gallery-data.js"
CACHE = ROOT / "gallery" / "places.js"

CONTACT = "jchi@pknu.ac.kr"          # Nominatim 정책상 연락처 필요
UA = f"iGDSL-website-geocoder/1.0 ({CONTACT})"
DELAY = 1.1                          # 요청 간격 (초) — 1초 이상 유지할 것


def read_place_names():
    """gallery-data.js 에서 place: '...' 값을 모두 뽑아냅니다."""
    if not DATA.exists():
        sys.exit(f"찾을 수 없음: {DATA}")
    text = DATA.read_text(encoding="utf-8")
    names = re.findall(r"""place\s*:\s*['"]([^'"]+)['"]""", text)
    seen, out = set(), []
    for n in names:
        n = n.strip()
        if n and n not in seen:
            seen.add(n)
            out.append(n)
    return out


def read_cache():
    """places.js 의 PLACES 객체를 읽어옵니다."""
    if not CACHE.exists():
        return {}, ""
    text = CACHE.read_text(encoding="utf-8")
    m = re.search(r"const\s+PLACES\s*=\s*(\{.*?\})\s*;", text, re.S)
    if not m:
        return {}, text
    body = m.group(1)
    body = re.sub(r"//[^\n]*", "", body)          # 주석 제거
    body = re.sub(r",(\s*\})", r"\1", body)       # 마지막 쉼표 제거
    try:
        return json.loads(body), text
    except json.JSONDecodeError as e:
        sys.exit(f"places.js 를 읽지 못했습니다: {e}")


def write_cache(places, original):
    """PLACES 객체만 새 내용으로 갈아끼웁니다 (설명 주석은 유지)."""
    lines = []
    for name in sorted(places):
        lat, lon = places[name]
        key = json.dumps(name, ensure_ascii=False)
        lines.append(f'  {key}: [{lat:.6f}, {lon:.6f}]')
    block = "const PLACES = {\n" + ",\n".join(lines) + "\n};"

    if original and re.search(r"const\s+PLACES\s*=\s*\{.*?\}\s*;", original, re.S):
        new = re.sub(r"const\s+PLACES\s*=\s*\{.*?\}\s*;", lambda _: block, original, flags=re.S)
    else:
        new = (original.rstrip() + "\n\n" if original else "") + block + "\n"
    CACHE.write_text(new, encoding="utf-8")


def geocode(name):
    """Nominatim 에 장소 이름 하나를 물어봅니다."""
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {"q": name, "format": "json", "limit": 1, "accept-language": "ko"}
    )
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        hits = json.loads(r.read().decode("utf-8"))
    if not hits:
        return None
    h = hits[0]
    return float(h["lat"]), float(h["lon"]), h.get("display_name", "")


def main():
    force = "--force" in sys.argv
    dry = "--dry-run" in sys.argv

    names = read_place_names()
    places, original = read_cache()

    if not names:
        print("gallery-data.js 에 place 이름이 없습니다.")
        return

    todo = names if force else [n for n in names if n not in places]
    print(f"장소 {len(names)}곳 중 {len(todo)}곳을 찾습니다.\n")

    if not todo:
        print("모두 좌표가 있습니다. 할 일이 없네요.")
        return

    found = failed = 0
    for i, name in enumerate(todo):
        if i:
            time.sleep(DELAY)
        try:
            hit = geocode(name)
        except Exception as e:
            print(f"  ✗ {name}  — 요청 실패: {e}")
            failed += 1
            continue
        if not hit:
            print(f"  ✗ {name}  — 검색 결과 없음")
            failed += 1
            continue
        lat, lon, label = hit
        places[name] = [round(lat, 6), round(lon, 6)]
        found += 1
        print(f"  ✓ {name}")
        print(f"      {lat:.6f}, {lon:.6f}   ({label[:70]})")

    print()
    if dry:
        print("--dry-run 이므로 파일은 바꾸지 않았습니다.")
    else:
        write_cache(places, original)
        print(f"places.js 저장 완료 — 찾음 {found}곳, 실패 {failed}곳")

    if failed:
        print("\n찾지 못한 장소는 이름을 더 구체적으로 바꿔보세요.")
        print("  예: '부경대' → '국립부경대학교 대연캠퍼스, 부산'")
        print("      '토론토'  → 'Metro Toronto Convention Centre, Toronto, Canada'")
        print("또는 places.js 에 좌표를 직접 적어도 됩니다.")


if __name__ == "__main__":
    main()
