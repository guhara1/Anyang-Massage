# 페이지별 검색 썸네일(og:image) 생성기. 다크 럭스 골드 테마, 1200x630.
# assets/og/{slug}.png (페이지별) + assets/og-image.png (메인/기본) 생성.
import os
from PIL import Image, ImageDraw, ImageFont

OUT = "assets/og"
os.makedirs(OUT, exist_ok=True)
W, H = 1200, 630
NAVY=(7,11,20); GOLD=(200,162,94); GOLD_SOFT=(233,215,171); TEXT=(234,237,244); DIM=(151,161,184)
KO="/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
SE="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
def ko(sz): return ImageFont.truetype(KO, sz)
def se(sz): return ImageFont.truetype(SE, sz)
PHONE="0508-202-4719"

# slug -> (tag, line1, line2)
PAGES = {
 # 행정구
 "manan-gu-chuljangmassage":   ("경기 · 안양", "만안구 출장마사지", "안양역 · 석수역 생활권"),
 "dongan-gu-chuljangmassage":  ("경기 · 안양", "동안구 출장마사지", "범계역 · 평촌역 · 인덕원역"),
 # 만안구 대표 행정동
 "anyang-dong-chuljangmassage":   ("경기 · 안양 만안", "안양동 출장마사지", "안양역 · 안양1번가"),
 "seoksu-dong-chuljangmassage":   ("경기 · 안양 만안", "석수동 출장마사지", "석수역 · 관악역 생활권"),
 "chunghun-dong-chuljangmassage": ("경기 · 안양 만안", "충훈동 출장마사지", "충훈부 주거권 방문 관리"),
 "bakdal-dong-chuljangmassage":   ("경기 · 안양 만안", "박달동 출장마사지", "박달동 차량 이동 생활권"),
 "hohyeon-dong-chuljangmassage":  ("경기 · 안양 만안", "호현동 출장마사지", "호현동 · 박달 인접 생활권"),
 # 동안구 대표 행정동
 "bisan-dong-chuljangmassage":    ("경기 · 안양 동안", "비산동 출장마사지", "비산사거리 · 종합운동장"),
 "buheung-dong-chuljangmassage":  ("경기 · 안양 동안", "부흥동 출장마사지", "평촌 인접 주거권"),
 "daran-dong-chuljangmassage":    ("경기 · 안양 동안", "달안동 출장마사지", "달안동 · 평촌 생활권"),
 "gwanyang-dong-chuljangmassage": ("경기 · 안양 동안", "관양동 출장마사지", "관양동 · 인덕원 인근"),
 "indeogwon-dong-chuljangmassage":("경기 · 안양 동안", "인덕원동 출장마사지", "인덕원역 중심 생활권"),
 "burim-dong-chuljangmassage":    ("경기 · 안양 동안", "부림동 출장마사지", "평촌역 · 안양시청 인근"),
 "pyeongchon-dong-chuljangmassage":("경기 · 안양 동안", "평촌동 출장마사지", "평촌학원가 · 주거권"),
 "pyeongan-dong-chuljangmassage": ("경기 · 안양 동안", "평안동 출장마사지", "평촌 아파트 생활권"),
 "gwiin-dong-chuljangmassage":    ("경기 · 안양 동안", "귀인동 출장마사지", "귀인동 · 평촌 주거권"),
 "hogye-dong-chuljangmassage":    ("경기 · 안양 동안", "호계동 출장마사지", "호계동 · 범계역 인근"),
 "beomgye-dong-chuljangmassage":  ("경기 · 안양 동안", "범계동 출장마사지", "범계역 중심 상권"),
 "sinchon-dong-chuljangmassage":  ("경기 · 안양 동안", "신촌동 출장마사지", "신촌동 · 호계 인접권"),
 "galsan-dong-chuljangmassage":   ("경기 · 안양 동안", "갈산동 출장마사지", "갈산동 · 평촌 인접권"),
 # 지하철역
 "seoksu-station-chuljangmassage":    ("경기 · 안양", "석수역 출장마사지", "석수동 · 서울 금천 인접권"),
 "gwanak-station-chuljangmassage":    ("경기 · 안양", "관악역 출장마사지", "안양예술공원 · 석수 생활권"),
 "anyang-station-chuljangmassage":    ("경기 · 안양", "안양역 출장마사지", "안양1번가 중심 상권"),
 "myeonghak-station-chuljangmassage": ("경기 · 안양", "명학역 출장마사지", "안양동 · 명학 생활권"),
 "indeogwon-station-chuljangmassage": ("경기 · 안양", "인덕원역 출장마사지", "관양동 · 인덕원 생활권"),
 "pyeongchon-station-chuljangmassage":("경기 · 안양", "평촌역 출장마사지", "평촌역 · 안양시청 주변"),
 "beomgye-station-chuljangmassage":   ("경기 · 안양", "범계역 출장마사지", "범계역 중심 상권"),
 # 안내 페이지
 "reservation": ("간다GO · 안양", "예약 안내", "방문 절차 · 이동비 · 결제 기준"),
 "guide":       ("간다GO · 안양", "이용 전 확인사항", "준비물 · 위생 · 안전 기준"),
 "hometai":     ("간다GO · 안양", "홈타이 이용 가이드", "진행 방식 · 추천 대상 안내"),
 "support":     ("간다GO · 안양", "고객센터", "공지 · 자주 묻는 질문 · 문의"),
}

# 메인/기본 og:image (assets/og-image.png)
MAIN = ("경기도 안양시 · 만안구 · 동안구", "안양 출장마사지 · 홈타이", "지역별 방문 예약 안내")


def fit(draw, text, font_factory, max_w, start, min_sz=40):
    sz=start
    while sz>min_sz:
        f=font_factory(sz); bb=draw.textbbox((0,0),text,font=f)
        if bb[2]-bb[0]<=max_w: return f
        sz-=4
    return font_factory(min_sz)

def ctext(d,cx,y,text,font,fill):
    bb=d.textbbox((0,0),text,font=font); w=bb[2]-bb[0]
    d.text((cx-w/2-bb[0], y), text, font=font, fill=fill)

def base(d):
    # top gold glow
    for i,r in enumerate(range(540,0,-44)):
        a=int(11*(1-i/13))
        if a>0: d.ellipse([600-r,-300-r//3,600+r,-300+r],fill=(200,162,94,a))
    # frame
    d.rectangle([24,24,W-25,H-25],outline=GOLD,width=3)
    d.rectangle([34,34,W-35,H-35],outline=(200,162,94,90),width=1)

def brandrow(d, cy=468):
    cx,R=600,40
    bf=ko(46); tb=d.textbbox((0,0),"간다GO",font=bf); btw=tb[2]-tb[0]
    gap=18; total=R*2+gap+btw; gx=600-total/2+R
    d.ellipse([gx-R,cy-R,gx+R,cy+R],fill=(10,17,32,255))
    d.ellipse([gx-R+3,cy-R+3,gx+R-3,cy+R-3],outline=GOLD,width=4)
    gf=se(50); gbb=d.textbbox((0,0),"G",font=gf)
    d.text((gx-(gbb[2]-gbb[0])/2-gbb[0], cy-(gbb[3]-gbb[1])/2-gbb[1]),"G",font=gf,fill=GOLD_SOFT)
    d.text((gx+R+gap, cy-(tb[3]-tb[1])/2-tb[1]),"간다GO",font=bf,fill=TEXT)

def phonepill(d):
    pt=f"예약전화  {PHONE}"; pf=ko(38); pb=d.textbbox((0,0),pt,font=pf); ptw=pb[2]-pb[0]
    qx0=600-ptw/2-34; qx1=600+ptw/2+34; qy0=536; qy1=536+62
    d.rounded_rectangle([qx0,qy0,qx1,qy1],radius=31,fill=GOLD)
    d.text((600-ptw/2-pb[0], qy0+(62-(pb[3]-pb[1]))/2-pb[1]), pt, font=pf, fill=(18,14,6))

def make(slug, tag, l1, l2):
    img=Image.new("RGB",(W,H),NAVY); d=ImageDraw.Draw(img,"RGBA")
    base(d)
    # tag pill (outline)
    tf=ko(30); bb=d.textbbox((0,0),tag,font=tf); tw=bb[2]-bb[0]
    px0=600-tw/2-26; px1=600+tw/2+26; py0=70; py1=70+54
    d.rounded_rectangle([px0,py0,px1,py1],radius=27,outline=GOLD,width=2)
    d.text((600-tw/2-bb[0], py0+(54-(bb[3]-bb[1]))/2-bb[1]), tag, font=tf, fill=GOLD_SOFT)
    # line1 (auto-fit), line2
    f1=fit(d,l1,ko,1000,96); ctext(d,600,196,l1,f1,GOLD_SOFT)
    f2=fit(d,l2,ko,1000,52); ctext(d,600,322,l2,f2,TEXT)
    # divider
    d.line([520,406,680,406],fill=GOLD,width=3)
    brandrow(d); phonepill(d)
    img.save(f"{OUT}/{slug}.png")
    return f"{OUT}/{slug}.png"

def make_main(tag, l1, l2):
    img=Image.new("RGB",(W,H),NAVY); d=ImageDraw.Draw(img,"RGBA")
    base(d)
    tf=ko(30); bb=d.textbbox((0,0),tag,font=tf); tw=bb[2]-bb[0]
    px0=600-tw/2-26; px1=600+tw/2+26; py0=68; py1=68+54
    d.rounded_rectangle([px0,py0,px1,py1],radius=27,outline=GOLD,width=2)
    d.text((600-tw/2-bb[0], py0+(54-(bb[3]-bb[1]))/2-bb[1]), tag, font=tf, fill=GOLD_SOFT)
    f1=fit(d,l1,ko,1040,92); ctext(d,600,192,l1,f1,GOLD_SOFT)
    f2=fit(d,l2,ko,1000,50); ctext(d,600,318,l2,f2,TEXT)
    d.line([520,404,680,404],fill=GOLD,width=3)
    brandrow(d); phonepill(d)
    img.save("assets/og-image.png")
    return "assets/og-image.png"

if __name__ == "__main__":
    for slug,(tag,l1,l2) in PAGES.items():
        print("wrote", make(slug,tag,l1,l2))
    print("wrote", make_main(*MAIN))
    print("done", len(PAGES)+1)
