# 사이트 공통 설정 — 배포 도메인: Netlify
BASE_URL = "https://anyang-massage.netlify.app"

BRAND = "간다GO"
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# 사이트 메타 — RSS·sitemap·IndexNow 에서 공통 사용
SITE_NAME = "간다GO 안양 출장마사지·홈타이"
SITE_DESC = "경기도 안양시 전지역(만안구·동안구) 방문 출장마사지·홈타이 지역별 예약 안내"

# IndexNow 키 — 빙·네이버·얀덱스·세즈남에 색인 즉시 통보 시 사용.
# 빌드 시 루트에 <KEY>.txt 파일이 생성되며, 키 변경 시 이 값만 바꾸면 된다.
INDEXNOW_KEY = "9049582cd9935ed2eb3f32736c5eeee0"

# 상단 메뉴 — 하위 메뉴에는 키워드를 반복하지 않고 지역명·역명만 표시한다.
# 구조: 안양시 → 행정구(만안구·동안구) → 대표 행정동 → 지하철역.
# 행정구는 허브 페이지를 두고, 대표 행정동/역 그룹의 부모는 메인 앵커로 묶는다.
NAV = [
    ("홈", "/", []),
    ("행정구별 안내", "/#districts", [
        ("만안구", "/anyang/manan-gu-chuljangmassage/"),
        ("동안구", "/anyang/dongan-gu-chuljangmassage/"),
    ]),
    ("대표 행정동별 안내", "/#areas", [
        ("안양동", "/anyang/manan/anyang-dong-chuljangmassage/"),
        ("석수동", "/anyang/manan/seoksu-dong-chuljangmassage/"),
        ("충훈동", "/anyang/manan/chunghun-dong-chuljangmassage/"),
        ("박달동", "/anyang/manan/bakdal-dong-chuljangmassage/"),
        ("호현동", "/anyang/manan/hohyeon-dong-chuljangmassage/"),
        ("비산동", "/anyang/dongan/bisan-dong-chuljangmassage/"),
        ("부흥동", "/anyang/dongan/buheung-dong-chuljangmassage/"),
        ("달안동", "/anyang/dongan/daran-dong-chuljangmassage/"),
        ("관양동", "/anyang/dongan/gwanyang-dong-chuljangmassage/"),
        ("인덕원동", "/anyang/dongan/indeogwon-dong-chuljangmassage/"),
        ("부림동", "/anyang/dongan/burim-dong-chuljangmassage/"),
        ("평촌동", "/anyang/dongan/pyeongchon-dong-chuljangmassage/"),
        ("평안동", "/anyang/dongan/pyeongan-dong-chuljangmassage/"),
        ("귀인동", "/anyang/dongan/gwiin-dong-chuljangmassage/"),
        ("호계동", "/anyang/dongan/hogye-dong-chuljangmassage/"),
        ("범계동", "/anyang/dongan/beomgye-dong-chuljangmassage/"),
        ("신촌동", "/anyang/dongan/sinchon-dong-chuljangmassage/"),
        ("갈산동", "/anyang/dongan/galsan-dong-chuljangmassage/"),
    ]),
    ("지하철역별 안내", "/#stations", [
        ("석수역", "/anyang/seoksu-station-chuljangmassage/"),
        ("관악역", "/anyang/gwanak-station-chuljangmassage/"),
        ("안양역", "/anyang/anyang-station-chuljangmassage/"),
        ("명학역", "/anyang/myeonghak-station-chuljangmassage/"),
        ("인덕원역", "/anyang/indeogwon-station-chuljangmassage/"),
        ("평촌역", "/anyang/pyeongchon-station-chuljangmassage/"),
        ("범계역", "/anyang/beomgye-station-chuljangmassage/"),
    ]),
    ("예약 안내", "/reservation/", []),
    ("이용 전 확인사항", "/guide/", []),
    ("홈타이 이용 가이드", "/hometai/", []),
    ("고객센터", "/support/", []),
]
