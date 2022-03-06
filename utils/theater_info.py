import urllib.request as req
import requests
import json
import pandas as pd
import re

from datetime import datetime as dt
from bs4 import BeautifulSoup as bs

from utils.kakao_map import KakaoMap

class Theater_Info:
    def __init__(self):
        self.date = dt.today().strftime("%Y%m%d")
        
        self.path = "../staticfiles/theater_code"
        self.Cgv_list = json.load(f"{self.path}/cgv.json")
        self.MegaBox_list = json.load(f"{self.path}/megabox.json")
        self.LotteCinema_list = json.load(f"{self.path}/megabox.json")

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
                    theater_code = self.Cgv_list[f'{cgv_theater}']['theaterCode']
                    areacode = 'None'
                    regioncode = self.Cgv_list[f'{cgv_theater}']['regioncode']
                elif theater['place_name'].find('DRIVE') != -1:
                    cgv_theater = theater['place_name']
                    theater_code = self.Cgv_list[f'{cgv_theater}']['theaterCode']
                    areacode = self.Cgv_list[f'{cgv_theater}']['areacode']
                    regioncode = 'None'
                else:
                    cgv_theater = re.sub(' |\n|\r|\t', '', theater['place_name'].strip())
                    theater_code = self.Cgv_list[f'{cgv_theater}']['theaterCode']
                    areacode = self.Cgv_list[f'{cgv_theater}']['areacode']
                    regioncode = 'None'
                theater_list[f'{cgv_theater}'] = self.CGV(theater_code, f'{areacode}', f'{regioncode}', cgv_theater, pos1, pos2, startaddr)
            elif name == '메가박스':
                if theater['place_name'].find('(') != -1:
                    continue
                else:
                    mega_theater = re.sub(' |\n|\r|\t', '', theater['place_name'].strip())
                    theater_code = self.MegaBox_list[f'{mega_theater[4:]}']['brchNo']
                theater_list[f'{mega_theater}'] = self.MegaBox(theater_code, mega_theater, pos1, pos2, startaddr)
            elif name == '롯데시네마':
                if theater['place_name'].find('(') != -1:
                    continue
                else:
                    lotte_theater = re.sub(' |\n|\r|\t', '', theater['place_name'].strip())
                    div_code = self.LotteCinema_list[f'{lotte_theater[5:]}']['divisionCode']
                    detaildiv_code = self.LotteCinema_list[f'{lotte_theater[5:]}']['detailDivisionCode']
                    cinema_code = self.LotteCinema_list[f'{lotte_theater[5:]}']['cinemaID']
                theater_list[f'{lotte_theater}'] = self.LotteCinema(div_code, detaildiv_code, cinema_code, lotte_theater, pos1, pos2, startaddr)   

        return theater_list