# 메인 페이지 — 안양시 전체 허브. 모든 키워드를 밀어 넣지 않고 행정구·행정동·역 페이지로 연결한다.
from .site import BASE_URL, BRAND, PHONE, PHONE_DISPLAY

# 실제 오프라인 매장 주소가 없으므로 LocalBusiness 대신 Organization 을 사용한다.
# 구조화 데이터(WebPage·Organization·Service·FAQ·후기·평점)는 build.py 가 전 페이지에
# 공통 @graph 로 자동 생성하므로 여기서는 검색엔진 사이트 소유확인 메타만 둔다.
# 네이버 서치어드바이저 소유확인 — 이전(pages.dev)·신규(netlify) 속성 모두 유지.
_JSONLD = """<meta name="naver-site-verification" content="359c3891ffb8e5fa3a6fc643301c0b77cbe3aa15" />
<meta name="naver-site-verification" content="44176af29c6d0b661818566816bcdb3a67642e40" />
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">Premium Visiting Spa · 경기도 안양시 전지역</p>
    <h1>안양 출장마사지 · 안양시 홈타이<br>지역별 예약 안내</h1>
    <p class="hero-lead">샵까지 갈 필요 없이, 계신 곳에서 받는 방문 관리.<br>만안구·동안구 어디든 전화 한 통이면 예약이 끝납니다.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/reservation/">예약 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>2개</strong><span>행정구 안내</span></li>
      <li><strong>18개</strong><span>대표 행정동</span></li>
      <li><strong>7개</strong><span>역세권 안내</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""

_BODY = f"""
<p class="lead">안양 출장마사지와 홈타이 예약을 찾는 분들을 위해 만안구·동안구 방문 가능 지역, 예약 절차, 이용 전 확인사항을 한곳에 정리했습니다. 이 페이지는 안양시 전체 구조를 설명하는 허브 역할을 하며, 자세한 내용은 행정구별·대표 행정동별·지하철역별 안내에서 확인하실 수 있습니다.</p>

<section id="why">
<h2>안양시에서 출장마사지를 찾는 이유</h2>
<p>안양 출장마사지를 찾는 분들은 대부분 현재 위치에서 가까운 방문 가능 지역을 먼저 확인합니다. 안양시는 만안구와 동안구로 나뉘고 두 생활권의 성격이 뚜렷하게 다릅니다. 만안구는 안양역·관악역·석수역·명학역을 중심으로 오래된 상권과 주거지가 함께 있는 지역이고, 동안구는 범계역·평촌역·인덕원역을 중심으로 상권과 업무지구, 아파트 단지, 학원가 수요가 함께 있는 지역입니다. 이렇게 동마다 성격이 달라서, 출장마사지를 찾는 분들도 본인 위치에서 가까운 방문 가능 지역을 먼저 확인하는 경우가 많습니다. 간다GO는 안양시 전지역을 대상으로 자택, 오피스텔, 숙소 어디든 관리사가 직접 방문하며, 샵을 오가는 이동 없이 계신 곳에서 바로 관리받고 그대로 쉴 수 있다는 점이 가장 큰 장점입니다.</p>
</section>

<section id="districts">
<h2>만안구·동안구 생활권 차이</h2>
<p>안양시는 행정구가 두 곳이므로 메인 페이지 아래에 먼저 행정구 페이지를 두고, 그 아래 대표 행정동 페이지와 지하철역 페이지를 연결하는 방식으로 구성했습니다. 만안구는 안양역과 안양1번가 상권, 석수역·관악역 생활권을 중심으로 한 안양의 원도심이고, 동안구는 평촌신도시를 중심으로 범계역 상권과 평촌 학원가, 인덕원 업무권이 자리한 계획도시 생활권입니다. 본인이 속한 행정구를 먼저 선택하시면 생활권에 맞는 안내를 확인하실 수 있습니다.</p>
<ul class="card-grid card-grid-rich">
<li><a href="/anyang/manan-gu-chuljangmassage/"><strong>만안구 출장마사지</strong><span>안양역·원도심 생활권</span></a></li>
<li><a href="/anyang/dongan-gu-chuljangmassage/"><strong>동안구 출장마사지</strong><span>평촌신도시·범계 상권</span></a></li>
</ul>
</section>

<section id="areas">
<h2>대표 행정동별 방문 가능 지역 안내</h2>
<p>지역 안내는 만안구 5개, 동안구 13개 대표 행정동을 기준으로 구성했습니다. 안양1동부터 안양9동까지는 안양동으로, 석수1·2동은 석수동으로, 비산1·2·3동은 비산동으로, 호계1·2·3동은 호계동으로 통합해 같은 생활권을 잘게 쪼개 비슷한 내용을 반복하지 않도록 정리했습니다. 거주하시거나 머무시는 동을 선택해 주세요.</p>
<p class="group-label">만안구</p>
<ul class="card-grid card-grid-rich">
<li><a href="/anyang/manan/anyang-dong-chuljangmassage/"><strong>안양동 출장마사지</strong><span>안양역·안양1번가</span></a></li>
<li><a href="/anyang/manan/seoksu-dong-chuljangmassage/"><strong>석수동 출장마사지</strong><span>석수역·관악역 생활권</span></a></li>
<li><a href="/anyang/manan/chunghun-dong-chuljangmassage/"><strong>충훈동 출장마사지</strong><span>충훈부 조용한 주거권</span></a></li>
<li><a href="/anyang/manan/bakdal-dong-chuljangmassage/"><strong>박달동 출장마사지</strong><span>차량 이동 외곽권</span></a></li>
<li><a href="/anyang/manan/hohyeon-dong-chuljangmassage/"><strong>호현동 출장마사지</strong><span>박달동 인접 주거권</span></a></li>
</ul>
<p class="group-label">동안구</p>
<ul class="card-grid card-grid-rich">
<li><a href="/anyang/dongan/bisan-dong-chuljangmassage/"><strong>비산동 출장마사지</strong><span>비산사거리·종합운동장</span></a></li>
<li><a href="/anyang/dongan/buheung-dong-chuljangmassage/"><strong>부흥동 출장마사지</strong><span>평촌 인접 주거권</span></a></li>
<li><a href="/anyang/dongan/daran-dong-chuljangmassage/"><strong>달안동 출장마사지</strong><span>달안동·평촌 생활권</span></a></li>
<li><a href="/anyang/dongan/gwanyang-dong-chuljangmassage/"><strong>관양동 출장마사지</strong><span>관양동·인덕원 인근</span></a></li>
<li><a href="/anyang/dongan/indeogwon-dong-chuljangmassage/"><strong>인덕원동 출장마사지</strong><span>인덕원역 중심 생활권</span></a></li>
<li><a href="/anyang/dongan/burim-dong-chuljangmassage/"><strong>부림동 출장마사지</strong><span>평촌역·안양시청 인근</span></a></li>
<li><a href="/anyang/dongan/pyeongchon-dong-chuljangmassage/"><strong>평촌동 출장마사지</strong><span>평촌학원가·주거권</span></a></li>
<li><a href="/anyang/dongan/pyeongan-dong-chuljangmassage/"><strong>평안동 출장마사지</strong><span>평촌 아파트 생활권</span></a></li>
<li><a href="/anyang/dongan/gwiin-dong-chuljangmassage/"><strong>귀인동 출장마사지</strong><span>귀인동·평촌 주거권</span></a></li>
<li><a href="/anyang/dongan/hogye-dong-chuljangmassage/"><strong>호계동 출장마사지</strong><span>호계동·범계역 인근</span></a></li>
<li><a href="/anyang/dongan/beomgye-dong-chuljangmassage/"><strong>범계동 출장마사지</strong><span>범계역 중심 상권</span></a></li>
<li><a href="/anyang/dongan/sinchon-dong-chuljangmassage/"><strong>신촌동 출장마사지</strong><span>신촌동·호계 인접</span></a></li>
<li><a href="/anyang/dongan/galsan-dong-chuljangmassage/"><strong>갈산동 출장마사지</strong><span>갈산동·평촌 인접권</span></a></li>
</ul>
</section>

<section id="stations">
<h2>안양역·범계역·평촌역·인덕원역 역세권 안내</h2>
<p>역을 기준으로 위치를 설명하는 것이 편하시다면 역세권 안내를 참고하세요. 안양역은 1호선 안양 원도심의 중심이고, 범계역·평촌역은 4호선 평촌신도시 생활권, 인덕원역은 4호선과 향후 광역철도가 더해질 교통 거점입니다. 석수역·관악역·명학역은 만안구 생활권을 잇습니다. 인덕원역처럼 여러 노선 계획이 있는 역도 노선별로 페이지를 나누지 않고 역마다 한 페이지로 안내합니다.</p>
<ul class="card-grid card-grid-rich">
<li><a href="/anyang/seoksu-station-chuljangmassage/"><strong>석수역 출장마사지</strong><span>석수동·서울 금천 인접</span></a></li>
<li><a href="/anyang/gwanak-station-chuljangmassage/"><strong>관악역 출장마사지</strong><span>안양예술공원·석수권</span></a></li>
<li><a href="/anyang/anyang-station-chuljangmassage/"><strong>안양역 출장마사지</strong><span>안양1번가 중심 상권</span></a></li>
<li><a href="/anyang/myeonghak-station-chuljangmassage/"><strong>명학역 출장마사지</strong><span>안양동·명학 생활권</span></a></li>
<li><a href="/anyang/indeogwon-station-chuljangmassage/"><strong>인덕원역 출장마사지</strong><span>관양동·인덕원권</span></a></li>
<li><a href="/anyang/pyeongchon-station-chuljangmassage/"><strong>평촌역 출장마사지</strong><span>평촌역·안양시청 주변</span></a></li>
<li><a href="/anyang/beomgye-station-chuljangmassage/"><strong>범계역 출장마사지</strong><span>범계역 중심 상권</span></a></li>
</ul>
</section>

<section id="hometai">
<h2>안양 홈타이 예약 전 확인사항</h2>
<p>안양 홈타이는 자택, 숙소, 사무실 인근에서 예약 가능 여부를 먼저 확인한 뒤 이용하는 방문형 관리 서비스입니다. 홈타이는 집에서 받는 타이마사지를 가리키는 말로, 오일을 쓰지 않고 편한 옷차림으로 받는 지압·스트레칭 구성이라 샤워 부담이 적어 처음 이용하는 분도 시작하기 좋습니다. 출장마사지와 홈타이는 형태가 조금 다를 뿐 예약 절차와 이용 기준은 같으므로, 어느 쪽을 원하시든 위치와 희망 시간만 알려주시면 됩니다. 진행 방식과 추천 대상, 받기 전 건강 확인 사항은 <a href="/hometai/">홈타이 이용 가이드</a>에서 자세히 정리했습니다. 예약 전에는 방문 가능 지역, 관리 가능 시간, 추가 이동비 여부, 결제 방식, 취소 기준을 함께 확인하시는 것이 좋으며, 자세한 내용은 <a href="/reservation/">예약 안내</a>에서 확인하실 수 있습니다.</p>
</section>

<section id="guide">
<h2>안양 출장마사지 사이트 이용 가이드</h2>
<p>이 사이트는 메인 페이지가 안양시 전체 안내를 맡고, 행정구 페이지가 만안구·동안구 생활권을, 대표 행정동 페이지가 세부 지역을, 역세권 페이지가 역 주변 안내를 각각 담당하도록 구성했습니다. 본인에게 익숙한 기준이 동이라면 행정동 페이지를, 역이라면 역 페이지를 보시면 되며 예약 절차와 이용 기준은 어느 쪽이든 동일합니다. 모든 안내는 과장 없이 방문 가능 지역, 예약 절차, 취소 기준, 개인정보 처리 기준을 분명히 보여 드리는 것을 원칙으로 하며, 불법적이거나 선정적인 요청, 무리한 요청은 어떤 경우에도 진행하지 않습니다.</p>
</section>

<section id="faq">
<h2>자주 묻는 질문</h2>
<div class="faq-item">
<h3>안양시 전지역 방문이 가능한가요?</h3>
<p>예약 시간, 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 만안구와 동안구 전지역을 대상으로 안내하며, 대표 행정동과 역세권 페이지에서 본인 위치에 맞는 기준을 확인하실 수 있습니다.</p>
</div>
<div class="faq-item">
<h3>만안구와 동안구는 무엇이 다른가요?</h3>
<p>만안구는 <a href="/anyang/anyang-station-chuljangmassage/">안양역</a>·관악역·석수역·명학역을 중심으로 한 원도심 상권과 주거지가, 동안구는 <a href="/anyang/beomgye-station-chuljangmassage/">범계역</a>·평촌역·인덕원역을 중심으로 상권과 학원가가 함께 있는 평촌신도시 생활권입니다.</p>
</div>
<div class="faq-item">
<h3>안양1동~9동, 호계1·2·3동은 왜 따로 없나요?</h3>
<p>번호로 나뉜 행정동은 안양동·호계동처럼 대표 행정동 페이지에서 통합 안내하여 중복 페이지 위험을 줄입니다. 예약은 주소 기준으로 진행되므로 행정동 번호를 모르셔도 됩니다.</p>
</div>
<div class="faq-item">
<h3>인덕원역은 노선이 여러 개인데 페이지가 하나인가요?</h3>
<p>네. <a href="/anyang/indeogwon-station-chuljangmassage/">인덕원역</a>은 향후 광역철도 계획이 있어도 안내 페이지 한 곳으로만 운영하고, 교통 특징은 본문에서 함께 설명합니다. 노선별로 페이지를 나누지 않습니다.</p>
</div>
<div class="faq-item">
<h3>홈타이와 출장마사지는 무엇이 다른가요?</h3>
<p>출장마사지는 관리사가 방문하는 형태 전체를, 홈타이는 그중 집에서 받는 타이마사지를 부르는 말입니다. 자세한 내용은 <a href="/hometai/">홈타이 이용 가이드</a>에서 확인하세요.</p>
</div>
</section>

<section id="contact" class="cta">
<h2>예약문의</h2>
<p>안양시 방문 관리 예약과 상담은 전화로 가장 빠르게 진행됩니다. 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "안양 출장마사지｜안양시 홈타이 지역별 예약 안내",
    "desc": "안양 출장마사지·홈타이 예약 전 만안구, 동안구, 역세권 정보를 정리했습니다.",
    "h1": "안양 출장마사지 · 안양시 홈타이 지역별 예약 안내",
    "body": _BODY,
    "extra_head": _JSONLD,
    "breadcrumb": [],
    "hero": _HERO,
}
