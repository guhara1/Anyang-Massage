#!/usr/bin/env python3
"""IndexNow 색인 즉시 통보 — 빙·네이버·얀덱스·세즈남 등 IndexNow 참여 검색엔진에
변경된 URL을 한 번에 알린다. 구글은 IndexNow 미참여(대신 Search Console/sitemap 사용).

준비물(빌드가 자동 처리):
  - content/site.py 의 INDEXNOW_KEY
  - 배포 후 https://<host>/<KEY>.txt 가 키 문자열을 그대로 반환해야 함(build.py 가 생성)

사용법:
  python3 scripts/indexnow.py                # sitemap.xml 의 모든 URL 통보
  python3 scripts/indexnow.py https://anyang-massage.netlify.app/anyang/manan/anyang-dong-chuljangmassage/
  python3 scripts/indexnow.py --dry-run      # 전송 없이 페이로드만 출력

엔드포인트는 api.indexnow.org 하나면 충분합니다(참여 엔진 전체로 전파됨).
한 번에 최대 10,000 URL. 같은 호스트의 URL만 보낼 수 있습니다.
"""
import json
import os
import re
import sys
import urllib.request
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL, INDEXNOW_KEY  # noqa: E402

ENDPOINT = "https://api.indexnow.org/IndexNow"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sitemap_urls():
    p = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(p):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python3 build.py` 를 실행하세요.")
    return re.findall(r"<loc>([^<]+)</loc>", open(p, encoding="utf-8").read())


def main(argv):
    dry = "--dry-run" in argv
    urls = [a for a in argv if a.startswith("http")]
    if not urls:
        urls = sitemap_urls()
    if not urls:
        sys.exit("통보할 URL이 없습니다.")

    host = urlparse(BASE_URL).netloc
    # 안전장치: 전부 같은 호스트인지 확인
    bad = [u for u in urls if urlparse(u).netloc != host]
    if bad:
        sys.exit(f"호스트가 다른 URL이 섞여 있습니다(IndexNow 불가): {bad[:3]}")

    payload = {
        "host": host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL.rstrip('/')}/{INDEXNOW_KEY}.txt",
        "urlList": urls,
    }
    print(f"IndexNow → {ENDPOINT}")
    print(f"  host={host}  urls={len(urls)}  key={INDEXNOW_KEY[:8]}…")
    if dry:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            code, body = r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        code, body = e.code, e.read().decode("utf-8", "ignore")
    print(f"HTTP {code}")
    if body.strip():
        print(body)
    # 200/202 = 접수, 400 = 키/형식 오류, 403 = 키 파일 검증 실패, 422 = URL/호스트 불일치, 429 = 과다
    if code in (200, 202):
        print("✓ 접수되었습니다. 참여 엔진(빙·네이버 등)으로 전파됩니다.")
    else:
        print("⚠ 실패. 키 파일 배포 여부와 호스트 일치를 확인하세요.")


if __name__ == "__main__":
    main(sys.argv[1:])
