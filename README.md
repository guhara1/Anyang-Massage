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

## 빠른 색인 / 인덱싱

빌드(`python3 build.py`)가 색인 채널 4종을 함께 생성합니다.

| 산출물 | 위치 | 용도 |
|--------|------|------|
| 사이트맵 | `/sitemap.xml` | `<lastmod>`·`<changefreq>`·`<priority>` 포함, 색인 32페이지 |
| RSS 피드 | `/rss.xml` | 검색엔진·피드 리더 발견 보조(전 페이지 `<head>`에 자동 링크) |
| robots | `/robots.txt` | 전체 허용 + Googlebot·Yeti(네이버)·bingbot·Daumoa 명시 + sitemap |
| IndexNow 키 | `/<KEY>.txt` | 빙·네이버·얀덱스 즉시 색인 통보용 키 검증 파일 |

### 글/페이지 올릴 때마다 (즉시 통보)
```bash
scripts/publish.sh                 # 빌드 + 전체 URL을 IndexNow로 통보
scripts/publish.sh <url> [<url>]   # 특정 URL만 통보
```
- **IndexNow**(`scripts/indexnow.py`): 빙·네이버·얀덱스·세즈남에 한 번에 전파. `--dry-run` 지원.
  배포(Cloudflare Pages)가 반영된 뒤 실행해야 `/<KEY>.txt` 검증이 통과합니다.
- **구글**(`scripts/google_indexing.py`): 구글은 IndexNow 미참여. Indexing API는 공식적으로
  JobPosting/BroadcastEvent 전용이라 일반 페이지 색인은 보장되지 않습니다. 일반 페이지의
  정석은 Search Console 등록 → `sitemap.xml` 제출 → 필요 시 URL 검사 도구 색인 요청입니다.
  (서비스 계정 설정 시 보조로 호출 가능 — 스크립트 상단 주석 참고.)
- 참고: 구글·빙의 `sitemap ping` 엔드포인트는 2023년에 폐지되어 사용하지 않습니다.
  IndexNow + Search Console/서치어드바이저 sitemap 제출이 그 자리를 대체합니다.

## 배포 전 해야 할 일

1. `content/site.py`의 `BASE_URL`은 `https://anyang-massage.netlify.app` 로 설정됨(변경 시 재빌드)
2. `python3 build.py` 재실행 (canonical·sitemap·rss·robots·IndexNow 키에 반영됨)
3. 네이버 서치어드바이저·구글 Search Console 사이트 등록 후 `sitemap.xml`·`rss.xml` 제출
4. 배포 반영 후 `scripts/publish.sh` 1회 실행으로 IndexNow 최초 통보
