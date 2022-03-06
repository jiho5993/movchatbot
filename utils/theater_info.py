import urllib.request as req
import requests
import json
import pandas as pd
import re

from datetime import datetime as dt
from bs4 import BeautifulSoup as bs

from utils.kakao_map import KakaoMap

Cgv_list = {
    "CGV강남": {
        "areacode": "01",
        "theaterCode": "0056"
    },
    "CGV강변": {
        "areacode": "01",
        "theaterCode": "0001"
    },
    "CGV건대입구": {
        "areacode": "01",
        "theaterCode": "0229"
    },
    "CGV구로": {
        "areacode": "01",
        "theaterCode": "0010"
    },
    "CGV대학로": {
        "areacode": "01",
        "theaterCode": "0063"
    },
    "CGV동대문": {
        "areacode": "01",
        "theaterCode": "0252"
    },
    "CGV등촌": {
        "areacode": "01",
        "theaterCode": "0230"
    },
    "CGV명동": {
        "areacode": "01",
        "theaterCode": "0009"
    },
    "CGV명동역씨네라이브러리": {
        "areacode": "01",
        "theaterCode": "0105"
    },
    "CGV목동": {
        "areacode": "01",
        "theaterCode": "0011"
    },
    "CGV미아": {
        "areacode": "01",
        "theaterCode": "0057"
    },
    "CGV불광": {
        "areacode": "01",
        "theaterCode": "0030"
    },
    "CGV상봉": {
        "areacode": "01",
        "theaterCode": "0046"
    },
    "CGV성신여대입구": {
        "areacode": "01",
        "theaterCode": "0300"
    },
    "CGV송파": {
        "areacode": "01",
        "theaterCode": "0088"
    },
    "CGV수유": {
        "areacode": "01",
        "theaterCode": "0276"
    },
    "CGV신촌아트레온": {
        "areacode": "01",
        "theaterCode": "0150"
    },
    "CGV압구정": {
        "areacode": "01",
        "theaterCode": "0040"
    },
    "CGV압구정본관":{
        "areacode": "01",
        "theaterCode": "0040"
    },
    "CGV여의도": {
        "areacode": "01",
        "theaterCode": "0112"
    },
    "CGV연남": {
        "areacode": "01",
        "theaterCode": "0292"
    },
    "CGV영등포": {
        "areacode": "01",
        "theaterCode": "0059"
    },
    "CGV왕십리": {
        "areacode": "01",
        "theaterCode": "0074"
    },
    "CGV용산아이파크몰": {
        "areacode": "01",
        "theaterCode": "0013"
    },
    "CGV중계": {
        "areacode": "01",
        "theaterCode": "0131"
    },
    "CGV천호": {
        "areacode": "01",
        "theaterCode": "0199"
    },
    "CGV청담씨네시티": {
        "areacode": "01",
        "theaterCode": "0107"
    },
    "CGV피카디리1958": {
        "areacode": "01",
        "theaterCode": "0223"
    },
    "CGV하계": {
        "areacode": "01",
        "theaterCode": "0164"
    },
    "CGV홍대": {
        "areacode": "01",
        "theaterCode": "0191"
    },
    "CINE de CHEF 압구정": {
        "regioncode": "103",
        "theaterCode": "0040"
    },
    "CINE de CHEF 용산아이파크몰": {
        "regioncode": "103",
        "theaterCode": "0013"
    },
    "CGV경기광주": {
        "areacode": "02",
        "theaterCode": "0260"
    },
    "CGV고양행신": {
        "areacode": "02",
        "theaterCode": "0255"
    },
    "CGV광교": {
        "areacode": "02",
        "theaterCode": "0257"
    },
    "CGV광교상현": {
        "areacode": "02",
        "theaterCode": "0266"
    },
    "CGV구리": {
        "areacode": "02",
        "theaterCode": "0232"
    },
    "CGV기흥": {
        "areacode": "02",
        "theaterCode": "0344"
    },
    "CGV김포": {
        "areacode": "02",
        "theaterCode": "0278"
    },
    "CGV김포운양": {
        "areacode": "02",
        "theaterCode": "0188"
    },
    "CGV김포한강": {
        "areacode": "02",
        "theaterCode": "0298"
    },
    "CGV동백": {
        "areacode": "02",
        "theaterCode": "0124"
    },
    "CGV동수원": {
        "areacode": "02",
        "theaterCode": "0041"
    },
    "CGV동탄": {
        "areacode": "02",
        "theaterCode": "0106"
    },
    "CGV동탄역": {
        "areacode": "02",
        "theaterCode": "0265"
    },
    "CGV동탄호수공원": {
        "areacode": "02",
        "theaterCode": "0233"
    },
    "CGV배곧": {
        "areacode": "02",
        "theaterCode": "0226"
    },
    "CGV범계": {
        "areacode": "02",
        "theaterCode": "0155"
    },
    "CGV부천": {
        "areacode": "02",
        "theaterCode": "0015"
    },
    "CGV부천역": {
        "areacode": "02",
        "theaterCode": "0194"
    },
    "CGV부천옥길": {
        "areacode": "02",
        "theaterCode": "0287"
    },
    "CGV북수원": {
        "areacode": "02",
        "theaterCode": "0049"
    },
    "CGV산본": {
        "areacode": "02",
        "theaterCode": "0242"
    },
    "CGV서현": {
        "areacode": "02",
        "theaterCode": "0196"
    },
    "CGV성남모란": {
        "areacode": "02",
        "theaterCode": "0304"
    },
    "CGV소풍": {
        "areacode": "02",
        "theaterCode": "0143"
    },
    "CGV수원": {
        "areacode": "02",
        "theaterCode": "0012"
    },
    "CGV스타필드시티위례": {
        "areacode": "02",
        "theaterCode": "0274"
    },
    "CGV시흥": {
        "areacode": "02",
        "theaterCode": "0073"
    },
    "CGV안산": {
        "areacode": "02",
        "theaterCode": "0211"
    },
    "CGV안성": {
        "areacode": "02",
        "theaterCode": "0279"
    },
    "CGV야탑": {
        "areacode": "02",
        "theaterCode": "0003"
    },
    "CGV양주옥정": {
        "areacode": "02",
        "theaterCode": "0262"
    },
    "CGV역곡": {
        "areacode": "02",
        "theaterCode": "0338"
    },
    "CGV오리": {
        "areacode": "02",
        "theaterCode": "0004"
    },
    "CGV오산": {
        "areacode": "02",
        "theaterCode": "0305"
    },
    "CGV오산중앙": {
        "areacode": "02",
        "theaterCode": "0307"
    },
    "CGV용인": {
        "areacode": "02",
        "theaterCode": "0271"
    },
    "CGV의정부": {
        "areacode": "02",
        "theaterCode": "0113"
    },
    "CGV의정부태흥": {
        "areacode": "02",
        "theaterCode": "0187"
    },
    "CGV이천": {
        "areacode": "02",
        "theaterCode": "0205"
    },
    "CGV일산": {
        "areacode": "02",
        "theaterCode": "0054"
    },
    "CGV정왕": {
        "areacode": "02",
        "theaterCode": "0320"
    },
    "CGV죽전": {
        "areacode": "02",
        "theaterCode": "0055"
    },
    "CGV파주문산": {
        "areacode": "02",
        "theaterCode": "0148"
    },
    "CGV파주야당": {
        "areacode": "02",
        "theaterCode": "0310"
    },
    "CGV판교": {
        "areacode": "02",
        "theaterCode": "0181"
    },
    "CGV평촌": {
        "areacode": "02",
        "theaterCode": "0195"
    },
    "CGV평택": {
        "areacode": "02",
        "theaterCode": "0052"
    },
    "CGV평택고덕": {
        "areacode": "02",
        "theaterCode": "0334"
    },
    "CGV평택소사": {
        "areacode": "02",
        "theaterCode": "0214"
    },
    "CGV포천": {
        "areacode": "02",
        "theaterCode": "0309"
    },
    "CGV하남미사": {
        "areacode": "02",
        "theaterCode": "0326"
    },
    "CGV화성봉담": {
        "areacode": "02",
        "theaterCode": "0301"
    },
    "CGV화정": {
        "areacode": "02",
        "theaterCode": "0145"
    },
    "CGV DRIVE IN 곤지암": {
        "areacode": "02",
        "theaterCode": "0342"
    },
    "CGV계양": {
        "areacode": "202",
        "theaterCode": "0043"
    },
    "CGV남주안": {
        "areacode": "202",
        "theaterCode": "0198"
    },
    "CGV부평": {
        "areacode": "202",
        "theaterCode": "0021"
    },
    "CGV송도타임스페이스": {
        "areacode": "202",
        "theaterCode": "0325"
    },
    "CGV연수역": {
        "areacode": "202",
        "theaterCode": "0247"
    },
    "CGV인천": {
        "areacode": "202",
        "theaterCode": "0002"
    },
    "CGV인천공항": {
        "areacode": "202",
        "theaterCode": "0118"
    },
    "CGV인천논현": {
        "areacode": "202",
        "theaterCode": "0254"
    },
    "CGV인천도화": {
        "areacode": "202",
        "theaterCode": "0340"
    },
    "CGV인천연수": {
        "areacode": "202",
        "theaterCode": "0258"
    },
    "CGV인천학익": {
        "areacode": "202",
        "theaterCode": "0269"
    },
    "CGV주안역": {
        "areacode": "202",
        "theaterCode": "0308"
    },
    "CGV청라": {
        "areacode": "202",
        "theaterCode": "0235"
    },
    "CGV DRIVE IN 스퀘어원": {
        "areacode": "202",
        "theaterCode": "0339"
    },
    "CGV강릉": {
        "areacode": "12",
        "theaterCode": "0139"
    },
    "CGV원주": {
        "areacode": "12",
        "theaterCode": "0144"
    },
    "CGV인제": {
        "areacode": "12",
        "theaterCode": "0281"
    },
    "CGV춘천": {
        "areacode": "12",
        "theaterCode": "0070"
    },
    "CGV논산": {
        "areacode": "03%2C205",
        "theaterCode": "0261"
    },
    "CGV당진": {
        "areacode": "03%2C205",
        "theaterCode": "0207"
    },
    "CGV대전": {
        "areacode": "03%2C205",
        "theaterCode": "0007"
    },
    "CGV대전가수원": {
        "areacode": "03%2C205",
        "theaterCode": "0286"
    },
    "CGV대전가오": {
        "areacode": "03%2C205",
        "theaterCode": "0154"
    },
    "CGV대전탄방": {
        "areacode": "03%2C205",
        "theaterCode": "0202"
    },
    "CGV대전터미널": {
        "areacode": "03%2C205",
        "theaterCode": "0127"
    },
    "CGV보령": {
        "areacode": "03%2C205",
        "theaterCode": "0275"
    },
    "CGV서산": {
        "areacode": "03%2C205",
        "theaterCode": "0091"
    },
    "CGV세종": {
        "areacode": "03%2C205",
        "theaterCode": "0219"
    },
    "CGV유성노은": {
        "areacode": "03%2C205",
        "theaterCode": "0206"
    },
    "CGV천안": {
        "areacode": "03%2C205",
        "theaterCode": "0044"
    },
    "CGV천안시청": {
        "areacode": "03%2C205",
        "theaterCode": "0332"
    },
    "CGV천안터미널": {
        "areacode": "03%2C205",
        "theaterCode": "0293"
    },
    "CGV천안펜타포트": {
        "areacode": "03%2C205",
        "theaterCode": "0110"
    },
    "CGV청주(서문)": {
        "areacode": "03%2C205",
        "theaterCode": "0228"
    },
    "CGV청주성안길": {
        "areacode": "03%2C205",
        "theaterCode": "0297"
    },
    "CGV청주율량": {
        "areacode": "03%2C205",
        "theaterCode": "0282"
    },
    "CGV청주지웰시티": {
        "areacode": "03%2C205",
        "theaterCode": "0142"
    },
    "CGV청주터미널": {
        "areacode": "03%2C205",
        "theaterCode": "0319"
    },
    "CGV충북혁신": {
        "areacode": "03%2C205",
        "theaterCode": "0284"
    },
    "CGV충주교현": {
        "areacode": "03%2C205",
        "theaterCode": "0328"
    },
    "CGV홍성": {
        "areacode": "03%2C205",
        "theaterCode": "0217"
    },
    "CGV대구수성": {
        "areacode": "11",
        "theaterCode": "0157"
    },
    "CGV대구스타디움": {
        "areacode": "11",
        "theaterCode": "0108"
    },
    "CGV대구아카데미": {
        "areacode": "11",
        "theaterCode": "0185"
    },
    "CGV대구연경": {
        "areacode": "11",
        "theaterCode": "0343"
    },
    "CGV대구월성": {
        "areacode": "11",
        "theaterCode": "0216"
    },
    "CGV대구칠곡": {
        "areacode": "11",
        "theaterCode": "0071"
    },
    "CGV대구한일": {
        "areacode": "11",
        "theaterCode": "0147"
    },
    "CGV대구현대": {
        "areacode": "11",
        "theaterCode": "0109"
    },
    "CGV대연": {
        "areacode": "05%2C207",
        "theaterCode": "0061"
    },
    "CGV동래": {
        "areacode": "05%2C207",
        "theaterCode": "0042"
    },
    "CGV부산명지": {
        "areacode": "05%2C207",
        "theaterCode": "0337"
    },
    "CGV서면": {
        "areacode": "05%2C207",
        "theaterCode": "0005"
    },
    "CGV서면삼정타워": {
        "areacode": "05%2C207",
        "theaterCode": "0285"
    },
    "CGV서면상상마당": {
        "areacode": "05%2C207",
        "theaterCode": "0303"
    },
    "CGV센텀시티": {
        "areacode": "05%2C207",
        "theaterCode": "0089"
    },
    "CGV아시아드": {
        "areacode": "05%2C207",
        "theaterCode": "0160"
    },
    "CGV울산동구": {
        "areacode": "05%2C207",
        "theaterCode": "0335"
    },
    "CGV울산삼산": {
        "areacode": "05%2C207",
        "theaterCode": "0128"
    },
    "CGV울산신천": {
        "areacode": "05%2C207",
        "theaterCode": "0264"
    },
    "CGV울산진장": {
        "areacode": "05%2C207",
        "theaterCode": "0246"
    },
    "CGV정관": {
        "areacode": "05%2C207",
        "theaterCode": "0306"
    },
    "CGV하단아트몰링": {
        "areacode": "05%2C207",
        "theaterCode": "0245"
    },
    "CGV해운대": {
        "areacode": "05%2C207",
        "theaterCode": "0318"
    },
    "CGV화명": {
        "areacode": "05%2C207",
        "theaterCode": "0159"
    },
    "CINE de CHEF 센텀": {
        "regioncode": "103",
        "theaterCode": "0089"
    },
    "CGV거제": {
        "areacode": "204",
        "theaterCode": "0263"
    },
    "CGV경산": {
        "areacode": "204",
        "theaterCode": "0330"
    },
    "CGV고성": {
        "areacode": "204",
        "theaterCode": "0323"
    },
    "CGV구미": {
        "areacode": "204",
        "theaterCode": "0053"
    },
    "CGV김천율곡": {
        "areacode": "204",
        "theaterCode": "0240"
    },
    "CGV김해": {
        "areacode": "204",
        "theaterCode": "0028"
    },
    "CGV김해율하": {
        "areacode": "204",
        "theaterCode": "0311"
    },
    "CGV김해장유": {
        "areacode": "204",
        "theaterCode": "0239"
    },
    "CGV마산": {
        "areacode": "204",
        "theaterCode": "0033"
    },
    "CGV북포항": {
        "areacode": "204",
        "theaterCode": "0097"
    },
    "CGV안동": {
        "areacode": "204",
        "theaterCode": "0272"
    },
    "CGV양산삼호": {
        "areacode": "204",
        "theaterCode": "0234"
    },
    "CGV진주혁신": {
        "areacode": "204",
        "theaterCode": "0324"
    },
    "CGV창원": {
        "areacode": "204",
        "theaterCode": "0023"
    },
    "CGV창원더시티": {
        "areacode": "204",
        "theaterCode": "0079"
    },
    "CGV창원상남": {
        "areacode": "204",
        "theaterCode": "0283"
    },
    "CGV통영": {
        "areacode": "204",
        "theaterCode": "0156"
    },
    "CGV포항": {
        "areacode": "204",
        "theaterCode": "0045"
    },
    "CGV광양": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0220"
    },
    "CGV광양엘에프스퀘어": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0221"
    },
    "CGV광주금남로": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0295"
    },
    "CGV광주상무": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0193"
    },
    "CGV광주용봉": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0210"
    },
    "CGV광주첨단": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0218"
    },
    "CGV광주충장로": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0244"
    },
    "CGV광주터미널": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0090"
    },
    "CGV광주하남": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0215"
    },
    "CGV군산": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0277"
    },
    "CGV나주": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0237"
    },
    "CGV목포": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0289"
    },
    "CGV목포평화광장": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0280"
    },
    "CGV서전주": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0225"
    },
    "CGV순천": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0114"
    },
    "CGV순천신대": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0268"
    },
    "CGV여수웅천": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0315"
    },
    "CGV익산": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0020"
    },
    "CGV전주고사": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0213"
    },
    "CGV전주에코시티": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0336"
    },
    "CGV전주효자": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0179"
    },
    "CGV정읍": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0186"
    },
    "CGV제주": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0302"
    },
    "CGV제주노형": {
        "areacode": "206%2C04%2C06",
        "theaterCode": "0259"
    }
}

MegaBox_list = {
    "강남": {
        "brchNo": "1372"
    },
    "강남대로씨티": {
        "brchNo": "0023"
    },
    "강동": {
        "brchNo": "1341"
    },
    "군자": {
        "brchNo": "1431"
    },
    "동대문": {
        "brchNo": "1003"
    },
    "마곡": {
        "brchNo": "1572"
    },
    "목동": {
        "brchNo": "1581"
    },
    "상봉": {
        "brchNo": "1311"
    },
    "상암월드컵경기장": {
        "brchNo": "1211"
    },
    "성수": {
        "brchNo": "1331"
    },
    "센트럴": {
        "brchNo": "1371"
    },
    "송파파크하비오": {
        "brchNo": "1381"
    },
    "신촌": {
        "brchNo": "1202"
    },
    "이수": {
        "brchNo": "1561"
    },
    "창동": {
        "brchNo": "1321"
    },
    "코엑스": {
        "brchNo": "1351"
    },
    "홍대": {
        "brchNo": "1212"
    },
    "화곡": {
        "brchNo": "1571"
    },
    "ARTNINE": {
        "brchNo": "1562"
    },
    "고양스타필드": {
        "brchNo": "4121"
    },
    "광명AK플라자": {
        "brchNo": "0029"
    },
    "김포한강신도시": {
        "brchNo": "4152"
    },
    "남양주": {
        "brchNo": "4721"
    },
    "남양주현대아울렛스페이스원": {
        "brchNo": "0019"
    },
    "동탄": {
        "brchNo": "4451"
    },
    "미사강변": {
        "brchNo": "4652"
    },
    "백석": {
        "brchNo": "4113"
    },
    "별내": {
        "brchNo": "4722"
    },
    "부천스타필드시티": {
        "brchNo": "4221"
    },
    "분당": {
        "brchNo": "4631"
    },
    "수원": {
        "brchNo": "0030"
    },
    "수원남문": {
        "brchNo": "4421"
    },
    "시흥배곧": {
        "brchNo": "4291"
    },
    "안산중앙": {
        "brchNo": "4253"
    },
    "안성스타필드": {
        "brchNo": "0020"
    },
    "양주": {
        "brchNo": "4821"
    },
    "영통": {
        "brchNo": "4431"
    },
    "용인기흥": {
        "brchNo": "0012"
    },
    "용인테크노밸리": {
        "brchNo": "4462"
    },
    "의정부민락": {
        "brchNo": "4804"
    },
    "일산": {
        "brchNo": "4111"
    },
    "일산벨라시타": {
        "brchNo": "4104"
    },
    "킨텍스": {
        "brchNo": "4112"
    },
    "파주금촌": {
        "brchNo": "4132"
    },
    "파주운정": {
        "brchNo": "4115"
    },
    "파주출판도시": {
        "brchNo": "4131"
    },
    "하남스타필드": {
        "brchNo": "4651"
    },
    "검단": {
        "brchNo": "4041"
    },
    "송도": {
        "brchNo": "4062"
    },
    "영종": {
        "brchNo": "4001"
    },
    "인천논현": {
        "brchNo": "4051"
    },
    "청라지젤": {
        "brchNo": "0027"
    },
    "공주": {
        "brchNo": "3141"
    },
    "논산": {
        "brchNo": "0018"
    },
    "대전": {
        "brchNo": "3021"
    },
    "대전신세계아트앤사이언스": {
        "brchNo": "0028"
    },
    "대전유성": {
        "brchNo": "0009"
    },
    "대전중앙로": {
        "brchNo": "3011"
    },
    "대전현대아울렛": {
        "brchNo": "0017"
    },
    "세종조치원": {
        "brchNo": "3391"
    },
    "세종나성": {
        "brchNo": "3392"
    },
    "세종청사": {
        "brchNo": "0008"
    },
    "오창": {
        "brchNo": "3631"
    },
    "제천": {
        "brchNo": "3901"
    },
    "진천": {
        "brchNo": "3651"
    },
    "천안": {
        "brchNo": "3301"
    },
    "청주사창": {
        "brchNo": "0013"
    },
    "충주": {
        "brchNo": "3801"
    },
    "홍성내포": {
        "brchNo": "3501"
    },
    "경북도청": {
        "brchNo": "7602"
    },
    "경산하양": {
        "brchNo": "7122"
    },
    "구미강동": {
        "brchNo": "7303"
    },
    "김천": {
        "brchNo": "7401"
    },
    "남포항": {
        "brchNo": "7901"
    },
    "대구": {
        "brchNo": "7022"
    },
    "대구신세계": {
        "brchNo": "7011"
    },
    "대구이시아": {
        "brchNo": "0022"
    },
    "덕천": {
        "brchNo": "6161"
    },
    "마산": {
        "brchNo": "6312"
    },
    "문경": {
        "brchNo": "7451"
    },
    "부산극장": {
        "brchNo": "6001"
    },
    "부산대": {
        "brchNo": "6906"
    },
    "북대구": {
        "brchNo": "0025"
    },
    "삼천포": {
        "brchNo": "6642"
    },
    "양산": {
        "brchNo": "6261"
    },
    "양산라피에스타": {
        "brchNo": "6262"
    },
    "울산": {
        "brchNo": "6811"
    },
    "정관": {
        "brchNo": "6191"
    },
    "창원": {
        "brchNo": "6421"
    },
    "창원내서": {
        "brchNo": "0014"
    },
    "해운대": {
        "brchNo": "6121"
    },
    "광주상무본관": {
        "brchNo": "5021"
    },
    "광주상무별관": {
        "brchNo": "5021"
    },
    "광주하남": {
        "brchNo": "5061"
    },
    "목포하당": {
        "brchNo": "5302"
    },
    "송천": {
        "brchNo": "5612"
    },
    "순천": {
        "brchNo": "5401"
    },
    "여수웅천": {
        "brchNo": "5552"
    },
    "전대": {
        "brchNo": "0010"
    },
    "전주혁신": {
        "brchNo": "0021"
    },
    "첨단": {
        "brchNo": "5064"
    },
    "남춘천": {
        "brchNo": "2001"
    },
    "속초": {
        "brchNo": "2171"
    },
    "원주": {
        "brchNo": "2201"
    },
    "원주센트럴": {
        "brchNo": "2202"
    }
}

LotteCinema_list = {
    "가산디지털": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1013"
    },
    "가양": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "9094"
    },
    "강동": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "9010"
    },
    "건대입구": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1004"
    },
    "김포공항": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1009"
    },
    "노원": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1003"
    },
    "도곡": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1023"
    },
    "독산": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1017"
    },
    "브로드웨이": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "9056"
    },
    "서울대입구": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1012"
    },
    "수락산": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "9099"
    },
    "수유": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "9104"
    },
    "신도림": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1015"
    },
    "신림": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1007"
    },
    "에비뉴엘": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1001"
    },
    "영등포": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1002"
    },
    "용산": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1014"
    },
    "월드타워": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1016"
    },
    "은평": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1021"
    },
    "중랑": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "9083"
    },
    "청량리": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1008"
    },
    "합정": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1010"
    },
    "홍대입구": {
        "divisionCode": "1",
        "detailDivisionCode": "1",
        "cinemaID": "1005"
    },
    "광교아울렛": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3030"
    },
    "광명": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3027"
    },
    "광명아울렛": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3025"
    },
    "광주터미널": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3020"
    },
    "구리아울렛": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3026"
    },
    "동탄": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3048"
    },
    "라페스타": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "9095"
    },
    "마석": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3021"
    },
    "별내": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3046"
    },
    "병점": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3017"
    },
    "부천": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3011"
    },
    "부천역": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "9054"
    },
    "부평": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3003"
    },
    "부평역사": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3008"
    },
    "북수원": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3045"
    },
    "산본피트인": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3031"
    },
    "서수원": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3043"
    },
    "성남중앙": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3041"
    },
    "센트럴락": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3012"
    },
    "송탄": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3029"
    },
    "수원": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3024"
    },
    "수지": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3044"
    },
    "시화": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "9088"
    },
    "시흥장현": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3049"
    },
    "안산": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3004"
    },
    "안산고잔": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3028"
    },
    "안성": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "9106"
    },
    "안양": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3007"
    },
    "안양일번가": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3032"
    },
    "영종하늘도시": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "9077"
    },
    "오산": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "9079"
    },
    "용인기흥": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3039"
    },
    "용인역북": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3040"
    },
    "위례": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3037"
    },
    "의정부민락": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3033"
    },
    "인덕원": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "9100"
    },
    "인천아시아드": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3035"
    },
    "인천터미널": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3038"
    },
    "주엽": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "9087"
    },
    "진접": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3010"
    },
    "파주운정": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3034"
    },
    "판교": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3047"
    },
    "평촌": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3018"
    },
    "평택비전": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "9075"
    },
    "하남미사": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "9096"
    },
    "향남": {
        "divisionCode": "1",
        "detailDivisionCode": "2",
        "cinemaID": "3036"
    },
    "당진": {
        "divisionCode": "1",
        "detailDivisionCode": "3",
        "cinemaID": "9085"
    },
    "대전": {
        "divisionCode": "1",
        "detailDivisionCode": "3",
        "cinemaID": "4002"
    },
    "대전관저": {
        "divisionCode": "1",
        "detailDivisionCode": "3",
        "cinemaID": "4009"
    },
    "대전둔산": {
        "divisionCode": "1",
        "detailDivisionCode": "3",
        "cinemaID": "4006"
    },
    "대전센트럴": {
        "divisionCode": "1",
        "detailDivisionCode": "3",
        "cinemaID": "4008"
    },
    "서산": {
        "divisionCode": "1",
        "detailDivisionCode": "3",
        "cinemaID": "9044"
    },
    "서청주": {
        "divisionCode": "1",
        "detailDivisionCode": "3",
        "cinemaID": "4004"
    },
    "아산터미널": {
        "divisionCode": "1",
        "detailDivisionCode": "3",
        "cinemaID": "4005"
    },
    "천안불당": {
        "divisionCode": "1",
        "detailDivisionCode": "3",
        "cinemaID": "9101"
    },
    "청주용암": {
        "divisionCode": "1",
        "detailDivisionCode": "3",
        "cinemaID": "4007"
    },
    "충주": {
        "divisionCode": "1",
        "detailDivisionCode": "3",
        "cinemaID": "9078"
    },
    "광주": {
        "divisionCode": "1",
        "detailDivisionCode": "4",
        "cinemaID": "6001"
    },
    "광주광산": {
        "divisionCode": "1",
        "detailDivisionCode": "4",
        "cinemaID": "9065"
    },
    "군산나운": {
        "divisionCode": "1",
        "detailDivisionCode": "4",
        "cinemaID": "6007"
    },
    "군산몰": {
        "divisionCode": "1",
        "detailDivisionCode": "4",
        "cinemaID": "6009"
    },
    "수완": {
        "divisionCode": "1",
        "detailDivisionCode": "4",
        "cinemaID": "6004"
    },
    "익산모현": {
        "divisionCode": "1",
        "detailDivisionCode": "4",
        "cinemaID": "9070"
    },
    "전주": {
        "divisionCode": "1",
        "detailDivisionCode": "4",
        "cinemaID": "6002"
    },
    "전주송천": {
        "divisionCode": "1",
        "detailDivisionCode": "4",
        "cinemaID": "9102"
    },
    "전주평화": {
        "divisionCode": "1",
        "detailDivisionCode": "4",
        "cinemaID": "6006"
    },
    "충장로": {
        "divisionCode": "1",
        "detailDivisionCode": "4",
        "cinemaID": "9047"
    },
    "경산": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "5008"
    },
    "경주": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "9090"
    },
    "경주황성": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "9091"
    },
    "구미공단": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "5013"
    },
    "대구광장": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "5012"
    },
    "대구율하": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "5006"
    },
    "대구현풍": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "9076"
    },
    "동성로": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "5005"
    },
    "상인": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "5016"
    },
    "상주": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "9080"
    },
    "성서": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "5004"
    },
    "영주": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "9064"
    },
    "영천": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "9098"
    },
    "포항": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "9097"
    },
    "프리미엄구미센트럴": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "9067"
    },
    "프리미엄만경": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "9066"
    },
    "프리미엄안동": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "9074"
    },
    "프리미엄칠곡": {
        "divisionCode": "1",
        "detailDivisionCode": "5",
        "cinemaID": "9057"
    },
    "거창": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "9082"
    },
    "광복": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "2009"
    },
    "김해부원": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "5015"
    },
    "김해아울렛": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "5011"
    },
    "대영": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "2012"
    },
    "동래": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "2007"
    },
    "동부산아울렛": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "2010"
    },
    "드라이브 오시리아": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "9093"
    },
    "마산(합성동)": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "9042"
    },
    "부산명지": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "9092"
    },
    "부산본점": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "2004"
    },
    "사천": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "9084"
    },
    "서면": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "2008"
    },
    "센텀시티": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "2006"
    },
    "양산물금": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "9103"
    },
    "엠비씨네": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "9069"
    },
    "오투": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "2011"
    },
    "울산": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "5001"
    },
    "울산성남": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "5014"
    },
    "진주혁신": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "5017"
    },
    "진해": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "5009"
    },
    "창원": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "5002"
    },
    "통영": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "9036"
    },
    "프리미엄경남대": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "9072"
    },
    "프리미엄진주": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "9003"
    },
    "프리미엄해운대": {
        "divisionCode": "1",
        "detailDivisionCode": "101",
        "cinemaID": "9059"
    },
    "남원주": {
        "divisionCode": "1",
        "detailDivisionCode": "6",
        "cinemaID": "7001"
    },
    "동해": {
        "divisionCode": "1",
        "detailDivisionCode": "6",
        "cinemaID": "7002"
    },
    "속초": {
        "divisionCode": "1",
        "detailDivisionCode": "6",
        "cinemaID": "9089"
    },
    "원주무실": {
        "divisionCode": "1",
        "detailDivisionCode": "6",
        "cinemaID": "7003"
    },
    "춘천": {
        "divisionCode": "1",
        "detailDivisionCode": "6",
        "cinemaID": "9081"
    },
    "서귀포": {
        "divisionCode": "1",
        "detailDivisionCode": "7",
        "cinemaID": "9013"
    },
    "제주삼화지구": {
        "divisionCode": "1",
        "detailDivisionCode": "7",
        "cinemaID": "9068"
    },
    "제주아라": {
        "divisionCode": "1",
        "detailDivisionCode": "7",
        "cinemaID": "9071"
    }
}

class Theater_Info:
    def __init__(self):
        self.date = dt.today().strftime("%Y%m%d")

    def CGV(self, theatercode, areacode, regioncode, name, pos1, pos2, startpos):
        event = 'http://www.cgv.co.kr/culture-event/event/defaultNew.aspx#1'
        if areacode == 'None':
            ticket = f'http://www.cgv.co.kr/theaters/special/show-times.aspx?regioncode={regioncode}&theatercode={theatercode}'
        if regioncode == 'None':
            ticket = f'http://www.cgv.co.kr/theaters/?areacode={areacode}&theatercode={theatercode}&date={self.date}'

        pos = dict(
            pos1=pos1,
            pos2=pos2
        )
        startpos = re.sub(' |\n|\r|\t', '', startpos.strip())
        nav_name = re.sub(' |\n|\r|\t', '', name.strip())
        nav = f'https://map.kakao.com/?sName={startpos}&eName={nav_name}'

        theater_list = dict(
            name=name,
            cinema=None,
            date=self.date,
            event=event,
            ticket=ticket,
            pos=pos,
            nav=nav
        )
        return theater_list

    def MegaBox(self, theatercode, name, pos1, pos2, startpos):
        event = 'https://www.megabox.co.kr/event'
        ticket = f'https://www.megabox.co.kr/theater?brchNo={theatercode}'
        
        pos = dict(
            pos1=pos1,
            pos2=pos2
        )
        startpos = re.sub(' |\n|\r|\t', '', startpos.strip())
        nav_name = re.sub(' |\n|\r|\t', '', name.strip())
        nav = f'https://map.kakao.com/?sName={startpos}&eName={nav_name}'

        theater_list = dict(
            name=name,
            cinema=None,
            date=self.date,
            event=event,
            ticket=ticket,
            pos=pos,
            nav=nav
        )
        return theater_list

    def LotteCinema(self, divcode, detaildiv_code, cinema_code, name, pos1, pos2, startpos):
        event = 'https://event.lottecinema.co.kr/NLCHS/Event'
        ticket = f'https://www.lottecinema.co.kr/NLCHS/Cinema/Detail?divisionCode={divcode}&detailDivisionCode={detaildiv_code}&cinemaID={cinema_code}'
        
        pos = dict(
            pos1=pos1,
            pos2=pos2
        )
        startpos = re.sub(' |\n|\r|\t', '', startpos.strip())
        nav_name = re.sub(' |\n|\r|\t', '', name.strip())
        nav = f'https://map.kakao.com/?sName={startpos}&eName={nav_name}'

        theater_list = dict(
            name=name,
            cinema=None,
            date=self.date,
            event=event,
            ticket=ticket,
            pos=pos,
            nav=nav
        )
        return theater_list

    def theater(self, startaddr, name):
        map_data = KakaoMap()
        theater_list = {}
        pos = map_data.addr_conv_pos(startaddr)
        if pos == None:
            return '잘못된 주소입니다.'
        if len(pos['documents']) == 0:
            return '잘못된 주소입니다.'
        x = pos['documents'][0]['x']
        y = pos['documents'][0]['y']
        startaddr = pos['documents'][0]['address_name']
        radius = 3000
        t_list = map_data.pos_conv_addr(name, x, y, radius)
        while len(t_list['documents']) < 2 and radius < 10000:
            radius += 1000
            t_list = map_data.pos_conv_addr(name, x, y, radius)
        if len(t_list['documents']) == 0:
            return '근처에 상영관이 존재하지 않습니다.'
        
        for theater in t_list['documents']:
            x = theater['x']
            y = theater['y']
            pos1 = theater['road_address_name']
            pos2 = theater['address_name']
            
            if name == 'cgv':
                if theater['place_name'].find('씨네드쉐프') != -1:
                    cgv_theater = "CINE de CHEF " + theater['place_name'].split()[-1]
                    theater_code = Cgv_list[f'{cgv_theater}']['theaterCode']
                    areacode = 'None'
                    regioncode = Cgv_list[f'{cgv_theater}']['regioncode']
                elif theater['place_name'].find('DRIVE') != -1:
                    cgv_theater = theater['place_name']
                    theater_code = Cgv_list[f'{cgv_theater}']['theaterCode']
                    areacode = Cgv_list[f'{cgv_theater}']['areacode']
                    regioncode = 'None'
                else:
                    cgv_theater = re.sub(' |\n|\r|\t', '', theater['place_name'].strip())
                    theater_code = Cgv_list[f'{cgv_theater}']['theaterCode']
                    areacode = Cgv_list[f'{cgv_theater}']['areacode']
                    regioncode = 'None'
                theater_list[f'{cgv_theater}'] = self.CGV(theater_code, f'{areacode}', f'{regioncode}', cgv_theater, pos1, pos2, startaddr)
            elif name == '메가박스':
                if theater['place_name'].find('(') != -1:
                    continue
                else:
                    mega_theater = re.sub(' |\n|\r|\t', '', theater['place_name'].strip())
                    theater_code = MegaBox_list[f'{mega_theater[4:]}']['brchNo']
                theater_list[f'{mega_theater}'] = self.MegaBox(theater_code, mega_theater, pos1, pos2, startaddr)
            elif name == '롯데시네마':
                if theater['place_name'].find('(') != -1:
                    continue
                else:
                    lotte_theater = re.sub(' |\n|\r|\t', '', theater['place_name'].strip())
                    div_code = LotteCinema_list[f'{lotte_theater[5:]}']['divisionCode']
                    detaildiv_code = LotteCinema_list[f'{lotte_theater[5:]}']['detailDivisionCode']
                    cinema_code = LotteCinema_list[f'{lotte_theater[5:]}']['cinemaID']
                theater_list[f'{lotte_theater}'] = self.LotteCinema(div_code, detaildiv_code, cinema_code, lotte_theater, pos1, pos2, startaddr)   

        return theater_list