#!/usr/bin/env bash
# 글/페이지를 올린 뒤 한 번에: 빌드 → 색인 즉시 통보(IndexNow).
# 사용: scripts/publish.sh                # 전체 sitemap URL 통보
#       scripts/publish.sh <url> [<url>]  # 특정 URL만 통보
# 배포(Cloudflare Pages)가 반영된 뒤 실행해야 키 파일 검증이 통과합니다.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 build.py
echo "----"
python3 scripts/indexnow.py "$@"

# 구글(선택, JobPosting/BroadcastEvent 외에는 보장 없음):
# 서비스 계정 설정 후 아래 주석을 해제하세요.
#   export GOOGLE_APPLICATION_CREDENTIALS=/path/service-account.json
#   python3 scripts/google_indexing.py "$@"
