# iGDSL 연구실 홈페이지

국립부경대학교 **지능형 공간데이터과학 연구실 (Intelligent Geospatial Data Science Lab)** 홈페이지입니다.
별도의 빌드 과정 없이 동작하는 정적 사이트로, GitHub Pages에 그대로 올려 사용할 수 있습니다.

---

## 1. GitHub Pages 배포

1. GitHub에서 새 저장소를 만듭니다. (예: `igdsl-pknu.github.io` 또는 `igdsl-web`)
2. 이 폴더의 **모든 파일**을 저장소 루트에 업로드하거나 push 합니다.

   ```bash
   git init
   git add .
   git commit -m "iGDSL 홈페이지"
   git branch -M main
   git remote add origin https://github.com/<계정>/<저장소>.git
   git push -u origin main
   ```

3. 저장소의 **Settings → Pages** 로 이동합니다.
4. *Source* 를 **Deploy from a branch**, *Branch* 를 **main / (root)** 로 지정하고 저장합니다.
5. 1~2분 뒤 `https://<계정>.github.io/<저장소>/` 에서 사이트가 열립니다.

> 저장소 이름이 `<계정>.github.io` 이면 주소는 `https://<계정>.github.io/` 가 됩니다.

---

## 2. 폴더 구조

```
.
├── index.html            홈 (히어로 → 연구 개요 → 최근 소식)
├── research.html         연구 (8개 분야)
├── people.html           구성원 (지도교수 / 재학생 / 졸업생)
├── publications.html     논문
├── news.html             소식
├── gallery.html          갤러리
├── contact.html          오시는 길
├── assets/
│   ├── style.css         전체 디자인
│   ├── site.js           공통 헤더·푸터·메뉴
│   ├── news-data.js      소식 데이터      ← 소식 추가는 여기
│   ├── pubs-data.js      논문 데이터      ← 논문 추가는 여기
│   └── keywords-data.js  연구 키워드 표   ← 키워드 추가는 여기
├── gallery/
│   ├── gallery-data.js   갤러리 목록      ← 사진 추가는 여기
│   ├── places.js         장소 좌표 캐시   ← geocode.py 가 자동으로 채웁니다
│   └── photos/           갤러리 사진 폴더 ← 사진 파일을 여기에
├── tools/
│   ├── geocode.py        장소 이름 → 좌표 변환 스크립트
│   └── keywords.py       (선택) 발표자료용 키워드 그림 생성
├── images/               로고 · 교수 사진 · 연구 다이어그램
│   └── crop/             연구 페이지에 인라인으로 쓰는 잘라낸 그림
└── .nojekyll
```

---

## 3. 내용 수정하기

HTML을 몰라도 아래 세 파일만 고치면 대부분의 내용이 갱신됩니다.

### 갤러리에 사진 추가

1. 사진 파일을 `gallery/photos/` 폴더에 넣습니다. (파일명은 영문·숫자·하이픈 권장)
2. `gallery/gallery-data.js` 의 `GALLERY = [` 바로 아래에 한 줄 추가합니다.

   ```js
   { file: '2026-isprs-01.jpg', date: '2026.07',
     title: 'XXV ISPRS Congress (캐나다 토론토)',
     desc: '연구실 구성원 5명이 참가해 연구결과를 발표했습니다.',
     album: '학회' },
   ```

3. push 하면 최신 날짜 순으로 자동 정렬되어 표시되고, `album` 값은 상단 필터 버튼이 됩니다.
   사진을 클릭하면 크게 보기(라이트박스)가 열립니다. ←/→ 로 넘기고 ESC 로 닫습니다.

| 항목 | 필수 | 설명 |
|---|---|---|
| `file` | ○ | `photos/` 안의 파일명 |
| `date` | ○ | `'2026.07'` 또는 `'2026.07.04'` — **월은 반드시 두 자리** |
| `title` | ○ | 사진 제목 |
| `desc` | | 한 줄 설명 |
| `album` | | 분류. 상단 필터 버튼이 됩니다 |
| `place` | | 촬영 장소 이름. 적으면 지도에 표시됩니다 |
| `loc` | | 좌표 `[위도, 경도]`. `place` 대신 직접 지정할 때만 |
| `pos` | | 목록 썸네일에서 보여줄 위치 (기본 `'center'`) |

> **월을 두 자리로** 적어야 합니다. 정렬이 글자 순서라 `'2026.7'` 은 `'2026.12'` 보다 위로 올라갑니다.

> 목록 썸네일은 **4:3으로 잘립니다.** 세로로 긴 사진에서 인물이 위아래로 치우쳤다면
> `pos: 'center 30%'` 처럼 조정하세요 (0% = 위쪽, 100% = 아래쪽).
> 크게 보기에서는 항상 원본 전체가 보입니다.

> 사진은 가로 **1600px 내외, 파일당 500KB 이하**로 줄여서 올리면 페이지가 빠릅니다.
> ImageMagick 이 있다면 `magick input.jpg -resize 1600x1600 -quality 85 output.jpg` 로 한 번에 줄일 수 있습니다.

### 촬영 위치 지도 (지오코딩)

사진에 `place` 로 **장소 이름만** 적으면 갤러리 상단에 장소 목록과 Google 위성지도가 나타납니다.
같은 `place` 끼리는 한 줄로 묶이고, 장소를 고르면 지도가 그 위치로 이동합니다.
"이 장소 사진 보기"를 누르면 그 장소의 사진이 크게 열립니다.
`place` 가 하나도 없으면 지도 영역 자체가 표시되지 않습니다.

좌표는 **`gallery/places.js`** 에 이름 → 좌표 표로 저장해 둡니다.
새 장소를 적었다면 홈페이지 폴더에서 한 번 실행하세요.

```bash
python3 tools/geocode.py              # 새 장소만 찾아서 places.js 에 추가
python3 tools/geocode.py --force      # 전부 다시 찾기
python3 tools/geocode.py --dry-run    # 결과만 확인, 파일은 그대로
```

OpenStreetMap Nominatim 으로 한 번 찾아 저장하는 방식이라, **방문자가 홈페이지를 열 때는
외부 지오코딩 호출이 전혀 없습니다.** (매번 호출하면 Nominatim 이용정책에 어긋나고 느립니다.)
지도 자체는 **Google 위성지도**를 API 키 없이 임베드합니다.

장소 이름이 모호하면 못 찾을 수 있습니다. 그럴 땐 이름을 구체적으로 바꾸거나

```
'부경대'  →  '국립부경대학교 대연캠퍼스, 부산'
'토론토'  →  'Metro Toronto Convention Centre, Toronto, Canada'
```

`places.js` 에 좌표를 직접 적어도 됩니다. 지오코딩 결과가 늘 정확하진 않으니
실행 후 지도에서 위치를 한 번 확인해 주세요.

> 사진 파일의 GPS 정보(EXIF)를 자동으로 읽는 방식은 넣지 않았습니다.
> 카카오톡·메일·클라우드를 거치면 GPS 태그가 대부분 지워지기 때문입니다.

**지도 종류 바꾸기** — `gallery.html` 의 `MAP_TYPE` 한 글자만 고치면 됩니다.
`contact.html` 은 iframe 주소의 `t=` 값을 바꾸면 됩니다.

| 값 | 지도 |
|---|---|
| `h` | 위성 + 지명·도로 라벨 **(현재 설정)** |
| `k` | 위성 (라벨 없음) |
| `m` | 일반 지도 |
| `p` | 지형 |

### 소식 추가

`assets/news-data.js` 에서 해당 연도 `items` 배열 **맨 위**에 한 줄 추가합니다.

```js
{ date: '10.15', cat: 'conf', text: '대한원격탐사학회 추계학술대회 참가 및 연구결과 발표',
  who: '지준화, 김보람' },
```

분류(`cat`)는 네 가지만 씁니다. 소식 페이지의 필터 버튼과 라벨 색이 여기서 결정됩니다.

| `cat` | 라벨 | 쓰는 경우 |
|---|---|---|
| `award` | 수상·선정 | 수상, 장학금·연구비·과제 선정 |
| `conf` | 학회 | 국내외 학회 참가 및 발표 |
| `intern` | 인턴십 | 외부 기관 인턴십 |
| `member` | 구성원 | 합류, 과정 시작, 졸업 |

홈 화면의 "최근 소식"에는 가장 위 5건이 자동으로 나옵니다.

### 학생 모집 배너

모든 페이지 맨 위에 표시되는 짙은 남색 띠입니다. `assets/site.js` 맨 위
`RECRUIT` 에서 문구와 링크를 고치고, 모집이 끝나면 `show: false` 로 바꾸면
전 페이지에서 사라집니다.

```js
const RECRUIT = {
  show: true,
  text:      'iGDSL에서 함께할 대학원 · 학·석사연계과정 학생을 모집합니다',
  textShort: '대학원 · 학·석사연계과정 학생 모집',   // 좁은 화면용
  cta:  '문의하기',
  href: 'mailto:jchi@pknu.ac.kr'
};
```

### 논문 추가

`assets/pubs-data.js` 배열 **맨 위**에 한 줄 추가합니다.

```js
{ year: 2026, type: 'intl',
  authors: 'Kim, B.-R., Chi, J.',
  title: '논문 제목',
  kw: ['Sea Ice', 'Deep Learning', 'Prediction'],
  venue: 'IEEE TGRS', detail: 'vol. 64, pp. 1–15',
  doi: 'https://doi.org/...' },
```

`type` 은 `'intl'`(국제학술지) 또는 `'dom'`(국내학술지)입니다.
연도별 묶음과 상단 편수 집계는 자동으로 갱신됩니다. `doi` 를 넣으면 제목이 링크가 됩니다.
`kw` 는 **논문마다 직접 정하는 주요 키워드**입니다 — 아래 설명을 보세요.

### 연구 키워드

논문 페이지 상단의 키워드 구름은 **각 논문의 `kw` 를 모아** 브라우저가 그 자리에서
나선형으로 배치해 그립니다. 돌릴 프로그램이 없고, 논문을 추가하면 크기와 편수가
저절로 바뀝니다. 키워드를 누르면 그 키워드가 달린 논문만 걸러집니다.

```js
kw: ['Sea Ice', 'Arctic', 'Prediction', 'Deep Learning', 'Time Series'],
```

**제목 글자와 상관없이 내용 기준으로 직접 정하면 됩니다.** 예를 들어 제목에
"deep learning" 이라는 말이 없는 ConvLSTM·SRGAN 논문도 `'Deep Learning'` 을 넣으면
함께 묶입니다. 이미 쓰던 이름을 그대로 쓰는 것이 중요합니다 — 철자가 한 글자라도
다르면 다른 키워드가 됩니다. (`'Sea Ice'` 와 `'sea ice'` 는 서로 다릅니다.)

한 논문에 3~5개 정도가 적당합니다. 너무 많으면 구름이 흐려집니다.

- **모바일**(760px 이하)에서는 편수 상위 18개만 더 큰 글자로 보여줍니다.
  개수는 `publications.html` 의 `counted.slice(0, 18)` 에서 바꿉니다.
- **배치**는 매번 같습니다. 글자 크기 범위는 `publications.html` 의 `sz()`,
  세로로 세우는 빈도는 `i % 5 === 3`, 단어 간격은 `pad` 에서 조절합니다.
- **색**은 `assets/style.css` 의 `.kwtag.s0` ~ `.s5` 입니다 (빈도 높을수록 진함).
- 발표자료용 그림 파일이 필요하면 `pip install wordcloud` 후 `python3 tools/keywords.py`
  를 실행하면 `images/keywords.png` 가 만들어집니다. 홈페이지에는 필요 없습니다.

### 개요 그림의 클릭 영역

홈·연구 페이지의 개요 다이어그램은 **그림 안의 각 연구 분야를 직접 누르면**
해당 설명으로 이동합니다. 영역은 `assets/site.js` 위쪽 `RESEARCH_AREAS` 에서
`[왼쪽%, 위%, 폭%, 높이%]` 로 정의합니다. 비율이라 화면 크기가 바뀌어도 맞습니다.

```js
{ n: '01', label: '위성정보 산출', box: [1.5, 16.5, 33.0, 19.0] },
```

그림을 새로 만들어 배치가 달라지면 이 숫자만 고치면 됩니다.
터치 기기에서는 마우스 올림 효과가 없으므로, 그림 아래 목록이 같은 역할을 합니다.

### 연구 그림 교체

연구 페이지의 그림은 두 벌을 씁니다.

- `images/0X-*.jpg` — 제목·태그가 포함된 원본. 그림을 **클릭하면** 이 원본이 크게 열립니다.
- `images/crop/0X-*.jpg` — 원본에서 위(제목 블록)와 아래(태그 밴드)를 잘라낸 것. 페이지에 인라인으로 보입니다.

원본을 새로 만들었다면 같은 이름으로 `images/`에 넣고, 아래 명령으로 잘라낸 버전을 다시 만듭니다.
(1280×720 기준으로 위 124px, 아래 65px을 잘라냅니다.)

```bash
python3 - <<'EOF'
from PIL import Image
import glob, os
os.makedirs('images/crop', exist_ok=True)
for f in sorted(glob.glob('images/0*-*.jpg')):
    im = Image.open(f)
    im.crop((0, 124, im.width, 655)).save('images/crop/' + os.path.basename(f), quality=90)
EOF
```

### 메뉴 변경

`assets/site.js` 맨 위의 `NAV` 배열만 고치면 모든 페이지의 메뉴가 함께 바뀝니다.

### 색상·글자 크기 변경

`assets/style.css` 맨 위 `:root` 영역에서 조정합니다.

```css
--navy:    #004d82;   /* 로고에서 추출한 브랜드 색 */
--fs-body: 19px;      /* 본문 기준 글자 크기 */
```

---

## 4. 로컬에서 미리 보기

`index.html` 을 브라우저에서 바로 열어도 동작합니다. 간단한 서버로 보려면:

```bash
python3 -m http.server 8000
# http://localhost:8000 접속
```

---

## 5. 로고 파일

| 파일 | 용도 |
|---|---|
| `images/logo.png` | 원본 로고 (흰 배경) |
| `images/logo-full.png` | 전체 로고, 배경 투명 |
| `images/logo-mark.png` | iGDSL 워드마크만, 배경 투명 (헤더용) |
| `images/favicon-512.png` / `-180` / `-32` | 지구본 심볼, 파비콘·앱 아이콘용 |
| `images/faculty-chi.jpg` | 지도교수 사진 (3:4, 720×960) |
