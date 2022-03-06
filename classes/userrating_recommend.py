import urllib.request as req
import requests

from bs4 import BeautifulSoup as bs

Genre_list = {
    '드라마' : '1',
    '판타지' : '2',
    '서부' : '3',
    '호러' : '4',
    '멜로' : '5',
    '애정' : '5',
    '로맨스' : '5',
    '모험' : '6',
    '스릴러' : '7',
    '느와르' : '8',
    '컬트' : '9',
    '다큐멘터리' : '10',
    '코미디' : '11',
    '가족' : '12',
    '미스터리' : '13',
    '전쟁' : '14',
    '애니메이션' : '15',
    '범죄' : '16',
    '뮤지컬' : '17',
    'SF' : '18',
    '액션' : '19',
    '무협' : '20',
    '에로' : '21',
    '서스펜스' : '22',
    '서사' : '23',
    '블랙코미디' : '24',
    '실험' : '25',
    '영화카툰' : '26',
    '영화음악' : '27',
    '영화패러디포스터' : '28'
}

class UserRating_Recommend:
    def __init__(self):
        self.NUM_CORES = 4

    def recommend(self, genre):
        if Genre_list.get(genre) == None:
            return
        url = f'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20220302&tg={Genre_list[genre]}'
        url_res = requests.get(url)
        soup = bs(url_res.text,'html.parser')
        cinema = soup.select("#old_content > table > tbody > tr > td > div.tit5 > a")
        cinema_list = []
        for i in cinema:
            cinema_list.append(i.get_text())
        return {'cinema' : cinema_list}