# 간다GO — 안양 출장마사지·홈타이 안내 사이트

경기도 안양시 전지역(만안구·동안구) 방문 관리(출장마사지·홈타이) 안내용 지역 SEO 정적 사이트입니다.
예약전화: **0508-202-4719**

## 구조

안양시는 행정구가 둘이므로 **안양시 → 행정구(만안구·동안구) → 대표 행정동 → 지하철역** 순서로 구성합니다.

- 정적 HTML 사이트 — GitHub Pages / Netlify / 일반 웹서버 어디서나 서빙 가능
- `build.py` + `content/` 패키지에서 페이지를 생성하는 빌드 방식
- 생성물(각 디렉터리의 `index.html`, `sitemap.xml`, `robots.txt`)도 저장소에 포함

```
build.py            # 빌드 스크립트 (레이아웃·목차·글자수 검사·sitemap 생성)
content/
  site.py           # 상호(간다GO)·전화·BASE_URL·메뉴 구조
  main.py           # 메인 페이지 (+ WebPage/BreadcrumbList/Organization/FAQPage JSON-LD)
  districts.py      # 행정구 2개 (만안구·동안구)
  areas_manan.py    # 만안구 대표 행정동 5개
  areas_dongan_a.py # 동안구 대표 행정동 7개
  areas_dongan_b.py # 동안구 대표 행정동 6개
  stations.py       # 지하철역 7개
  info.py           # 예약 안내·이용 전 확인사항·홈타이 가이드·고객센터·개인정보 처리방침
assets/             # CSS, 모바일 내비 JS, 파비콘, OG 이미지
scripts/gen_thumbs.py  # 페이지별 검색 썸네일(og:image) 생성기 (Pillow)
```

## 페이지 구성 (총 33개)

| 구분 | 수 | URL 예시 |
|------|----|----------|
| 메인 | 1 | `/` |
| 행정구 | 2 | `/anyang/manan-gu-chuljangmassage/`, `/anyang/dongan-gu-chuljangmassage/` |
| 만안구 대표 행정동 | 5 | `/anyang/manan/anyang-dong-chuljangmassage/` |
| 동안구 대표 행정동 | 13 | `/anyang/dongan/beomgye-dong-chuljangmassage/` |
| 지하철역 | 7 | `/anyang/anyang-station-chuljangmassage/` |
| 안내 | 4 | `/reservation/`, `/guide/`, `/hometai/`, `/support/` |
| 정책(noindex) | 1 | `/privacy/` |

대표 행정동 통합 규칙: 안양1~9동 → **안양동**, 석수1·2동 → **석수동**, 비산1·2·3동 → **비산동**,
호계1·2·3동 → **호계동** 으로 통합(번호 동 개별 페이지 없음).

## 빌드

```bash
python3 build.py          # HTML·sitemap·robots 생성, 페이지별 글자수·색인 리포트 출력
python3 scripts/gen_thumbs.py   # assets/og/*.png + assets/og-image.png 재생성 (Pillow 필요)
```

## SEO 운영 원칙 (빌드에 강제됨)

- 본문 **2,000자 미만 페이지는 자동 `noindex`** 처리되고 sitemap에서 제외
- 모든 페이지 **메타 디스크립션 80자 이내**
- 행정동은 대표 동 단위만 — 번호 행정동(안양1동·호계1동 등) 개별 페이지 없음
- 역은 역 1개당 페이지 1개 — 환승·예정 노선(GTX-C·월곶판교선·인덕원동탄선·신안산선)도
  노선별 페이지 없이 해당 역 본문의 **보조 설명**으로만 처리, 개통 전 예정역 단독 색인 페이지 금지
- **지역+역+테마 조합 페이지 없음** (도어웨이 방지)
- 실제 오프라인 매장 주소가 없으므로 **LocalBusiness 대신 Organization Schema** 사용
- 모든 페이지 본문은 페이지별 고유 작성 (지역명만 바꾼 복붙 없음)

## 배포 전 해야 할 일

1. `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경
2. `python3 build.py` 재실행 (canonical·sitemap·robots.txt에 반영됨)
3. Google Search Console / 네이버 서치어드바이저에 `sitemap.xml` 제출
