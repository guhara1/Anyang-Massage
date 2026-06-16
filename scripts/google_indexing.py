#!/usr/bin/env python3
"""구글 Indexing API 로 URL 색인/갱신을 통보한다.

⚠ 중요 — 공식 제약:
  구글 Indexing API 는 공식적으로 JobPosting / BroadcastEvent(라이브) 구조화 데이터
  페이지에만 지원됩니다. 일반 지역/안내 페이지는 이 API로 보내도 색인을 보장하지
  않습니다. 일반 페이지의 정석은 (1) Search Console 사이트 등록 → (2) sitemap.xml 제출
  → (3) 필요 시 URL 검사 도구로 색인 요청 입니다. 이 스크립트는 그 위에 '추가로'
  쓰는 보조 수단이며, 빙·네이버 즉시 색인은 IndexNow(scripts/indexnow.py)를 쓰세요.

사전 준비(1회):
  1) Google Cloud 프로젝트에서 'Indexing API' 사용 설정
  2) 서비스 계정 생성 → JSON 키 발급
  3) Search Console 속성에 그 서비스 계정 이메일을 '소유자'로 추가
  4) pip install google-auth requests

사용법:
  export GOOGLE_APPLICATION_CREDENTIALS=/path/service-account.json
  python3 scripts/google_indexing.py                 # sitemap.xml 전체 URL_UPDATED
  python3 scripts/google_indexing.py <url> [<url> …]  # 지정 URL만
  python3 scripts/google_indexing.py --delete <url>   # URL_DELETED 통보

쿼터: 기본 하루 200건. 대량은 batch(여기선 순차 호출)로 처리합니다.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def sitemap_urls():
    p = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(p):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python3 build.py` 를 실행하세요.")
    return re.findall(r"<loc>([^<]+)</loc>", open(p, encoding="utf-8").read())


def main(argv):
    try:
        import requests
        from google.auth.transport.requests import AuthorizedSession
        from google.oauth2 import service_account
    except ImportError:
        sys.exit("의존성이 없습니다. `pip install google-auth requests` 후 다시 실행하세요.")

    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred_path or not os.path.exists(cred_path):
        sys.exit("GOOGLE_APPLICATION_CREDENTIALS 환경변수에 서비스 계정 JSON 경로를 지정하세요.")

    action = "URL_DELETED" if "--delete" in argv else "URL_UPDATED"
    urls = [a for a in argv if a.startswith("http")] or sitemap_urls()

    creds = service_account.Credentials.from_service_account_file(cred_path, scopes=SCOPES)
    session = AuthorizedSession(creds)

    ok = 0
    for u in urls:
        r = session.post(API, json={"url": u, "type": action}, timeout=30)
        tag = "✓" if r.status_code == 200 else "✗"
        print(f"{tag} {r.status_code} {action} {u}")
        if r.status_code != 200:
            print("   ", r.text[:300])
        else:
            ok += 1
    print(f"\n완료: {ok}/{len(urls)} 성공")
    if ok < len(urls):
        print("실패가 있으면 서비스 계정의 Search Console '소유자' 권한과 API 사용 설정을 확인하세요.")


if __name__ == "__main__":
    main(sys.argv[1:])
