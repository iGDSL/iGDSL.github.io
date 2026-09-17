/* =========================================================
   iGDSL — 공통 헤더 / 푸터
   메뉴를 바꾸려면 아래 NAV 배열만 수정하면 모든 페이지에 반영됩니다.
   ========================================================= */

/* 모든 페이지 상단에 표시되는 모집 배너.
   내리려면 show 를 false 로 바꾸면 됩니다. */
const RECRUIT = {
  show: true,
  text:      'iGDSL에서 함께할 대학원 · 학·석사연계과정 학생을 모집합니다',
  textShort: '대학원 · 학·석사연계과정 학생 모집',   // 좁은 화면용
  cta:  '문의하기',
  href: 'mailto:jchi@pknu.ac.kr?subject=%5BiGDSL%5D%20%EB%8C%80%ED%95%99%EC%9B%90%20%EC%A7%84%ED%95%99%20%EB%AC%B8%EC%9D%98'
};

/* 개요 다이어그램의 8개 연구 분야 클릭 영역
   box = [왼쪽%, 위%, 폭%, 높이%] — 그림 크기가 바뀌어도 비율이라 그대로 맞습니다. */
const RESEARCH_AREAS = [
  { n: '01', label: '위성정보 산출',        box: [1.5, 16.5, 33.0, 19.0] },
  { n: '02', label: '시공간 변화 예측',      box: [1.5, 35.5, 33.0, 17.0] },
  { n: '03', label: '위성영상 품질 향상',    box: [1.5, 52.5, 33.0, 17.0] },
  { n: '04', label: '매칭·정합·이동 추적',   box: [1.5, 69.5, 33.0, 19.5] },
  { n: '05', label: '변화탐지',             box: [62.0, 16.5, 36.5, 19.0] },
  { n: '06', label: '학습영상 생성',        box: [62.0, 35.5, 36.5, 17.0] },
  { n: '07', label: '다종센서 무인기 활용',  box: [62.0, 52.5, 36.5, 17.0] },
  { n: '08', label: '위성 파운데이션 모델',  box: [60.0, 69.5, 38.5, 19.5] }
];

const NAV = [
  { href: 'index.html',        label: '홈' },
  { href: 'research.html',     label: '연구' },
  { href: 'people.html',       label: '구성원' },
  { href: 'publications.html', label: '논문' },
  { href: 'news.html',         label: '소식' },
  { href: 'gallery.html',      label: '갤러리' },
  { href: 'contact.html',      label: '오시는 길' }
];

(function () {
  const here = (location.pathname.split('/').pop() || 'index.html').toLowerCase();

  /* ---------- 모집 배너 (전 페이지 공통) ---------- */
  if (RECRUIT.show) {
    const bar = document.createElement('a');
    bar.className = 'recruitbar';
    bar.href = RECRUIT.href;
    bar.innerHTML = `
      <span class="wrap">
        <span class="dot" aria-hidden="true"></span>
        <span class="msg full">${RECRUIT.text}</span>
        <span class="msg short">${RECRUIT.textShort || RECRUIT.text}</span>
        <span class="cta">${RECRUIT.cta} <span aria-hidden="true">→</span></span>
      </span>`;
    document.body.insertBefore(bar, document.body.firstChild);
  }

  /* ---------- header ---------- */
  const header = document.querySelector('header.site');
  if (header) {
    header.innerHTML = `
      <div class="headbar">
        <a class="brand" href="index.html">
          <img src="images/logo-mark.png" alt="iGDSL 로고">
          <span class="bt">
            <b>지능형 공간데이터과학 연구실</b>
            <span>Intelligent Geospatial Data Science Lab · PKNU</span>
          </span>
        </a>
        <button class="navtoggle" aria-expanded="false" aria-controls="mainnav">☰ 메뉴</button>
        <nav class="mainnav" id="mainnav">
          ${NAV.map(n =>
            `<a href="${n.href}"${n.href.toLowerCase() === here ? ' class="active" aria-current="page"' : ''}>${n.label}</a>`
          ).join('')}
        </nav>
      </div>`;

    const btn = header.querySelector('.navtoggle');
    const nav = header.querySelector('.mainnav');
    btn.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
    });
  }

  /* ---------- 개요 다이어그램 클릭 영역 ----------
     <div class="overview-frame" data-hotspots="research.html"> 가 있으면
     그림 위에 8개 연구 분야로 가는 투명한 링크를 얹습니다. */
  document.querySelectorAll('[data-hotspots]').forEach(frame => {
    const base = frame.dataset.hotspots || '';
    frame.insertAdjacentHTML('beforeend', RESEARCH_AREAS.map((a, i) => {
      const [l, t, w, h] = a.box;
      return `<a class="hotspot" href="${base}#s${i + 1}"
                 style="left:${l}%;top:${t}%;width:${w}%;height:${h}%"
                 aria-label="${a.label} 연구 자세히 보기">
                <span class="hs-tag"><b>${a.n}</b>${a.label}</span>
              </a>`;
    }).join(''));
  });

  /* ---------- footer ----------
     푸터는 각 HTML 파일에 그대로 들어 있습니다. 검색엔진이 자바스크립트를
     실행하지 않아도 페이지 간 링크를 따라갈 수 있게 하기 위해서입니다.
     내용을 바꾸려면 7개 html 파일의 <footer class="site"> 블록을 함께 고치세요.
     여기서는 연도만 현재 값으로 맞춥니다. */
  document.querySelectorAll('footer.site .yr').forEach(el => {
    el.textContent = new Date().getFullYear();
  });

})();


/* =========================================================
   공용 라이트박스 (연구 그림 / 갤러리 사진 공통)

   사용법 1 — HTML에서 자동 연결:
     <figure class="figure zoomable" data-zoom
             data-full="images/01.jpg" data-title="제목" data-desc="설명">
   사용법 2 — 스크립트에서 직접 호출:
     Lightbox.open([{src, title, desc}, ...], 0)
   ========================================================= */

window.Lightbox = (function () {
  let el, imgEl, titleEl, descEl;
  let items = [], idx = 0;

  function build() {
    if (el) return;
    el = document.createElement('div');
    el.className = 'lb';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-modal', 'true');
    el.setAttribute('aria-label', '이미지 크게 보기');
    el.innerHTML = `
      <button class="close" aria-label="닫기">✕</button>
      <button class="prev" aria-label="이전">‹</button>
      <button class="next" aria-label="다음">›</button>
      <figure><img alt=""><figcaption><b></b><span></span></figcaption></figure>`;
    document.body.appendChild(el);

    imgEl   = el.querySelector('img');
    titleEl = el.querySelector('figcaption b');
    descEl  = el.querySelector('figcaption span');

    el.querySelector('.close').addEventListener('click', close);
    el.querySelector('.prev').addEventListener('click', () => show(idx - 1));
    el.querySelector('.next').addEventListener('click', () => show(idx + 1));
    el.addEventListener('click', e => { if (e.target === el) close(); });

    document.addEventListener('keydown', e => {
      if (!el.classList.contains('on')) return;
      if (e.key === 'Escape')     close();
      if (e.key === 'ArrowLeft')  show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  function show(i) {
    idx = (i + items.length) % items.length;
    const it = items[idx];
    imgEl.src = it.src;
    imgEl.alt = it.title || '';
    titleEl.textContent = it.title || '';
    descEl.textContent  = it.desc  || '';
    const solo = items.length < 2;
    el.querySelector('.prev').hidden = solo;
    el.querySelector('.next').hidden = solo;
  }

  function open(list, i) {
    if (!list || !list.length) return;
    build();
    items = list;
    show(i || 0);
    el.classList.add('on');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    el.classList.remove('on');
    document.body.style.overflow = '';
  }

  /* data-zoom 자동 연결 */
  document.addEventListener('DOMContentLoaded', () => {
    const nodes = [...document.querySelectorAll('[data-zoom]')];
    if (!nodes.length) return;

    const list = nodes.map(n => ({
      src:   n.dataset.full || n.querySelector('img')?.getAttribute('src'),
      title: n.dataset.title || '',
      desc:  n.dataset.desc  || ''
    }));

    nodes.forEach((n, i) => {
      n.tabIndex = 0;
      n.setAttribute('role', 'button');
      n.setAttribute('aria-label', (list[i].title || '이미지') + ' 크게 보기');
      n.addEventListener('click', () => open(list, i));
      n.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(list, i); }
      });
    });
  });

  return { open, close };
})();
