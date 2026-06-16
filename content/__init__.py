# 전체 페이지 목록 집계
# 구조: 메인 1 + 행정구 2 + 대표 행정동 18(만안 5 + 동안 13) + 지하철역 7 + 안내 5 = 33
from . import (
    main,
    districts,
    areas_manan,
    areas_dongan_a,
    areas_dongan_b,
    stations,
    info,
)

PAGES = (
    [main.PAGE]
    + districts.PAGES
    + areas_manan.PAGES
    + areas_dongan_a.PAGES
    + areas_dongan_b.PAGES
    + stations.PAGES
    + info.PAGES
)
