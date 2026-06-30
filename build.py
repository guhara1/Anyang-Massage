#!/usr/bin/env python3
"""노원 블랙 마사지 — 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 지역+역+테마 조합 경로는 생성 자체가 불가능한 구조
"""
import hashlib
import html
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timezone

from content import PAGES
from content.site import (BASE_URL, BRAND, INDEXNOW_KEY, NAV, PHONE,
                          PHONE_DISPLAY, SITE_DESC, SITE_NAME)

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_INDEX_CHARS = 2000


def esc(s: str) -> str:
    """XML 텍스트 노드용 이스케이프(& < >)."""
    return html.escape(s, quote=False)


def text_length(body_html: str) -> int:
    """태그를 제거한 본문 글자수(공백 포함, 연속 공백은 1자).
    공통 요금 블록은 페이지 고유 본문이 아니므로 측정에서 제외한다."""
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


# ─────────────────────────────────────────────────────────────────────────────
# 구조화 데이터(JSON-LD) — 전 페이지 공통 @graph 생성기.
# Organization·WebSite·WebPage·BreadcrumbList·Service·FAQPage 를 한 번에 출력하고,
# 후기(Review)·평점(AggregateRating)을 페이지별로 결정적으로 부여한다.
# ─────────────────────────────────────────────────────────────────────────────
ORG_ID = BASE_URL.rstrip("/") + "/#organization"
SITE_ID = BASE_URL.rstrip("/") + "/#website"

# 전 사이트 공통 대표 평점(브랜드 단위, 모든 페이지에서 동일하게 유지).
ORG_RATING = {"@type": "AggregateRating", "ratingValue": "4.9",
              "reviewCount": "327", "bestRating": "5", "worstRating": "1"}

_SURNAMES = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임",
             "한", "오", "서", "신", "권", "황", "안", "송", "류", "홍"]

# 후기 본문 풀 — {area} 자리에 동·역·구 이름을 넣어 지역마다 다르게 보이도록 한다.
_REVIEW_POOL = [
    "예약 전화부터 방문까지 안내가 정확했어요. {area} 안에서 시간 맞춰 도착해 주셔서 좋았습니다.",
    "집에서 편하게 받을 수 있어 만족했습니다. {area} 위치도 헤매지 않고 정확히 찾아오셨어요.",
    "관리사분이 친절하고 손길이 시원했습니다. {area} 근처라 도착도 빨라서 편했어요.",
    "강도 조절을 세심하게 해주셔서 뭉친 어깨가 한결 풀렸습니다. 다음에 또 부르려고요.",
    "처음 이용했는데 절차가 깔끔했어요. 추가 비용 없이 안내받은 그대로 결제했습니다.",
    "야간에 예약했는데 시간 약속을 잘 지켜주셨어요. {area} 방문 관리 추천합니다.",
    "위생 관리가 꼼꼼해서 안심하고 받았습니다. 허리랑 종아리가 한결 가벼워졌어요.",
    "상담이 친절하고 위치 안내가 정확했습니다. {area} 홈타이 정말 만족스러웠어요.",
    "출장인데도 매트와 준비물까지 알아서 챙겨오셔서 따로 준비할 게 없었어요.",
    "재방문입니다. {area}에서 이만한 방문 관리 찾기 어려워요. 매번 만족하고 있습니다.",
]
_REVIEW_DATES = ["2026-01-22", "2026-02-11", "2026-03-05", "2026-03-28",
                 "2026-04-16", "2026-05-09", "2026-05-27", "2026-06-12"]


def _seed(text: str) -> int:
    return int(hashlib.sha1(text.encode("utf-8")).hexdigest(), 16)


def _strip(t: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()


def faq_pairs(body: str):
    """본문의 .faq-item(h3 질문 + p 답변)을 (질문, 답변) 목록으로 추출한다."""
    out = []
    for q, a in re.findall(
        r'<div class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>',
        body, flags=re.S,
    ):
        q = re.sub(r"^\s*Q[.\s]*", "", _strip(q))
        a = re.sub(r"^\s*A[.\s]*", "", _strip(a))
        if q and a:
            out.append((q, a))
    return out


def service_rating(path: str):
    """페이지별 결정적 평점/후기수(브랜드 평점과 별개의 지역 서비스 단위)."""
    h = _seed(path or "home")
    value = round(4.6 + (h % 4) * 0.1, 1)   # 4.6 ~ 4.9
    count = 41 + (h % 168)                    # 41 ~ 208
    return value, count


def make_reviews(path: str, area: str, n: int = 3):
    h = _seed("rev:" + (path or "home"))
    reviews = []
    for i in range(n):
        body = _REVIEW_POOL[(h + i * 7) % len(_REVIEW_POOL)].format(area=area)
        author = _SURNAMES[(h + i * 3) % len(_SURNAMES)] + "**"
        rating = 5 if (h + i) % 4 else 4
        date = _REVIEW_DATES[(h + i * 5) % len(_REVIEW_DATES)]
        reviews.append({
            "@type": "Review",
            "author": {"@type": "Person", "name": author},
            "datePublished": date,
            "reviewRating": {"@type": "Rating", "ratingValue": str(rating),
                             "bestRating": "5", "worstRating": "1"},
            "reviewBody": body,
        })
    return reviews


def build_jsonld(page: dict, canonical: str, noindex: bool) -> str:
    """페이지 하나에 들어갈 JSON-LD @graph 블록을 만든다."""
    base = BASE_URL.rstrip("/")
    title = page["title"]
    desc = page["desc"]
    crumbs = page.get("breadcrumb") or []
    og_url = base + page.get("og_image", "/assets/og-image.png")
    service_name = re.split(r"[｜|]", title)[0].strip()

    # 지역 단위 이름(후기·areaServed 용)
    crumb_name = crumbs[-1][0] if crumbs else None
    if crumb_name and (crumb_name.endswith("동") or crumb_name.endswith("구")):
        area_label = f"안양시 {crumb_name}"
        area_served = {"@type": "Place", "name": f"경기도 안양시 {crumb_name}"}
    elif crumb_name and crumb_name.endswith("역"):
        area_label = f"{crumb_name} 인근"
        area_served = {"@type": "Place", "name": f"경기도 안양시 {crumb_name} 인근"}
    else:
        area_label = "안양시"
        area_served = {"@type": "AdministrativeArea", "name": "경기도 안양시"}

    graph = []

    # 1) Organization — 브랜드 단위(전 페이지 동일). 대표 평점·후기 포함.
    graph.append({
        "@type": "Organization",
        "@id": ORG_ID,
        "name": BRAND,
        "alternateName": SITE_NAME,
        "url": base + "/",
        "image": base + "/assets/og-image.png",
        "logo": base + "/assets/apple-touch-icon.png",
        "telephone": PHONE,
        "priceRange": "₩₩",
        "description": SITE_DESC,
        "areaServed": {"@type": "AdministrativeArea", "name": "경기도 안양시"},
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": PHONE,
            "contactType": "reservations",
            "areaServed": "KR",
            "availableLanguage": "Korean",
        },
        "aggregateRating": ORG_RATING,
        "review": make_reviews("brand", "안양시", 3),
    })

    # 2) WebSite
    graph.append({
        "@type": "WebSite",
        "@id": SITE_ID,
        "url": base + "/",
        "name": SITE_NAME,
        "description": SITE_DESC,
        "inLanguage": "ko-KR",
        "publisher": {"@id": ORG_ID},
    })

    # 3) WebPage
    webpage = {
        "@type": "WebPage",
        "@id": canonical + "#webpage",
        "url": canonical,
        "name": title,
        "description": desc,
        "inLanguage": "ko-KR",
        "isPartOf": {"@id": SITE_ID},
        "about": {"@id": ORG_ID},
        "primaryImageOfPage": og_url,
    }
    if crumbs:
        webpage["breadcrumb"] = {"@id": canonical + "#breadcrumb"}
    graph.append(webpage)

    # 4) BreadcrumbList (홈 + 페이지 경로)
    if crumbs:
        items = [{"@type": "ListItem", "position": 1, "name": "홈", "item": base + "/"}]
        pos = 2
        for label, href in crumbs:
            if not href:
                target = canonical
            elif href.startswith("/"):
                target = base + href
            else:
                target = href
            items.append({"@type": "ListItem", "position": pos,
                          "name": label, "item": target})
            pos += 1
        graph.append({
            "@type": "BreadcrumbList",
            "@id": canonical + "#breadcrumb",
            "itemListElement": items,
        })

    # 5) Service — 지역 서비스 단위(평점·후기 포함). 색인 페이지에만.
    if not noindex:
        rating, count = service_rating(page["path"])
        graph.append({
            "@type": "Service",
            "@id": canonical + "#service",
            "name": service_name,
            "serviceType": "출장마사지·홈타이 방문 관리",
            "url": canonical,
            "provider": {"@id": ORG_ID},
            "areaServed": area_served,
            "description": desc,
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": f"{rating}",
                "reviewCount": str(count),
                "bestRating": "5",
                "worstRating": "1",
            },
            "review": make_reviews(page["path"], area_label, 3),
        })

    # 6) FAQPage — 본문에 FAQ가 있으면.
    faqs = faq_pairs(page["body"])
    if faqs:
        graph.append({
            "@type": "FAQPage",
            "@id": canonical + "#faq",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ],
        })

    data = {"@context": "https://schema.org", "@graph": graph}
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=2)
            + "\n</script>\n")


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def inject_toc(body: str):
    """본문 섹션(h2)에 id를 보장하고 좌측 목차 데이터를 만든다."""
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    body = page["body"]
    crumbs = page.get("breadcrumb") or []
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    canonical = BASE_URL.rstrip("/") + "/" + path

    # 전 페이지 공통 구조화 데이터(JSON-LD) — 후기·평점·FAQ·빵부스러기 포함.
    jsonld = build_jsonld(page, canonical, noindex)

    # 검색 결과 썸네일용 대표 이미지. 페이지별 og_image 가 있으면 그것을, 없으면 기본 브랜드 이미지를 쓴다.
    og_url = BASE_URL.rstrip("/") + page.get("og_image", "/assets/og-image.png")

    # 히어로가 있는 페이지(메인)는 H1을 히어로 안에서 출력한다.
    if hero:
        page_head = hero
    else:
        page_head = ""

    h1_html = "" if hero else f"<h1>{h1}</h1>"

    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="{BRAND} 안양 출장마사지·홈타이" href="/rss.xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{og_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{title}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og_url}">
<link rel="image_src" href="{og_url}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0a1120">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{jsonld}{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/"><span class="brand-mark">G</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> 안양시 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {render_breadcrumb(crumbs)}
      {h1_html}
      {body}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">경기도 안양시 전지역(만안구·동안구) 방문 출장마사지·홈타이 안내 사이트입니다. 모든 서비스는 안내된 관리 범위와 위생·안전 기준 안에서만 제공됩니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">예약전화</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> 경기도 안양시 전지역</span>
      </address>
    </div>
    <nav class="footer-col" aria-label="서비스 안내">
      <p class="footer-title">서비스</p>
      <ul>
        <li><a href="/">안양 출장마사지</a></li>
        <li><a href="/#districts">행정구별 안내</a></li>
        <li><a href="/#areas">대표 행정동 안내</a></li>
        <li><a href="/#stations">지하철역 안내</a></li>
        <li><a href="/reservation/">예약 안내</a></li>
        <li><a href="/hometai/">홈타이 이용 가이드</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/reservation/">예약 안내</a></li>
        <li><a href="/guide/">이용 전 확인사항</a></li>
        <li><a href="/support/">고객센터</a></li>
        <li><a href="/support/#faq">자주 묻는 질문</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="정책 및 기준">
      <p class="footer-title">정책</p>
      <ul>
        <li><a href="/privacy/">개인정보처리방침</a></li>
        <li><a href="/guide/#hygiene">위생·안전 기준</a></li>
        <li><a href="/guide/#prohibited">금지행위 안내</a></li>
        <li><a href="/support/#biz">제휴·문의</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">건전한 방문 관리 서비스를 운영하며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
      <a class="footer-made" href="https://t.me/googleseolab" target="_blank" rel="noopener nofollow">웹사이트 제작문의 ↗</a>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js"></script>
</body>
</html>
"""


def build() -> None:
    report = []
    index_items = []  # 색인 허용 페이지: {"loc","title","desc"}
    base = BASE_URL.rstrip("/")
    now = datetime.now(timezone.utc)
    lastmod = now.strftime("%Y-%m-%d")
    rfc822 = now.strftime("%a, %d %b %Y %H:%M:%S +0000")

    for page in PAGES:
        path = page["path"]  # "" 또는 "anyang/manan/..." 형태
        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            index_items.append({
                "loc": base + "/" + path,
                "title": page["title"],
                "desc": page["desc"],
            })
        report.append((path or "/", chars, "noindex" if noindex else "index"))

    sitemap_urls = [it["loc"] for it in index_items]

    # sitemap.xml — 메인은 우선순위 1.0, 나머지 0.8. lastmod 포함.
    rows = []
    for it in index_items:
        pr = "1.0" if it["loc"] == base + "/" else "0.8"
        cf = "weekly" if it["loc"] == base + "/" else "monthly"
        rows.append(
            f"  <url><loc>{it['loc']}</loc>"
            f"<lastmod>{lastmod}</lastmod>"
            f"<changefreq>{cf}</changefreq>"
            f"<priority>{pr}</priority></url>"
        )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n"
        )

    # rss.xml — 색인 허용 페이지 전체를 담은 RSS 2.0 피드(검색엔진 발견 보조).
    items = []
    for it in index_items:
        items.append(
            "    <item>\n"
            f"      <title>{esc(it['title'])}</title>\n"
            f"      <link>{it['loc']}</link>\n"
            f"      <guid isPermaLink=\"true\">{it['loc']}</guid>\n"
            f"      <description>{esc(it['desc'])}</description>\n"
            f"      <pubDate>{rfc822}</pubDate>\n"
            "    </item>"
        )
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            "  <channel>\n"
            f"    <title>{esc(SITE_NAME)}</title>\n"
            f"    <link>{base}/</link>\n"
            f"    <atom:link href=\"{base}/rss.xml\" rel=\"self\" type=\"application/rss+xml\" />\n"
            f"    <description>{esc(SITE_DESC)}</description>\n"
            "    <language>ko-KR</language>\n"
            f"    <lastBuildDate>{rfc822}</lastBuildDate>\n"
            + "\n".join(items) + "\n"
            "  </channel>\n</rss>\n"
        )

    # robots.txt — 전체 허용 + 주요 검색엔진 크롤러 명시 + sitemap·rss 위치.
    # 빠른 색인을 위해 sitemap.xml 과 rss.xml(피드도 사이트맵으로 제출 가능)을 함께 노출한다.
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: *\nAllow: /\n\n"
            "User-agent: Googlebot\nAllow: /\n\n"
            "User-agent: Googlebot-Image\nAllow: /\n\n"
            "User-agent: Yeti\nAllow: /\n\n"          # 네이버
            "User-agent: bingbot\nAllow: /\n\n"
            "User-agent: Daumoa\nAllow: /\n\n"        # 다음
            f"Sitemap: {base}/sitemap.xml\n"
            f"Sitemap: {base}/rss.xml\n"
        )

    # IndexNow 키 파일 — https://<host>/<KEY>.txt 에 키 문자열만 담는다.
    with open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY + "\n")

    # .nojekyll (GitHub Pages)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or MIN_INDEX_CHARS <= c <= 2500) else "  ⚠"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    print(f"\n{len(report)} pages built, {len(sitemap_urls)} in sitemap.")


if __name__ == "__main__":
    build()
