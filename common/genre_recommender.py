import requests
import json
import re

from datetime import datetime as dt
from bs4 import BeautifulSoup as bs

class GenreRecommender:
    def __init__(self, genre):
        # 현재 날짜
        self.date = dt.today().strftime("%Y%m%d")
        
        with open("./staticfiles/genre/genre.json", "r") as file:
            self.Genre_list = json.load(file)
        
        self.genre = genre
        self.genre_index = self.Genre_list[genre]

    def recommend(self):
        # 존재하지 않는 장르일경우, 올바르지 못한 입력일경우
        if self.Genre_list.get(self.genre) == None:
            return None

        # 현재 날짜에 맞는 입력된 장르의 유저 평점순 정렬된 웹 페이지 크롤링
        url = f'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cnt&date={self.date}&tg={self.genre_index}'

        url_res = requests.get(url)
        soup = bs(url_res.text,'html.parser')
        cinema = soup.select("table.list_ranking > tbody > tr > td.title")

        cinema_list = []

        for i in cinema:
            title = re.sub('\n', '', i.get_text())
            link = i.select_one("a")['href']

            cinema_list.append({
                'title': title,
                'link': f'https://movie.naver.com{link}'
            })

        return cinema_list