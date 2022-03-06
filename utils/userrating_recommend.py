import urllib.request as req
import requests
import json

from bs4 import BeautifulSoup as bs

class UserRating_Recommend:
    def __init__(self):
        self.NUM_CORES = 4

        self.path = "../staticfiles/genre"
        self.Genre_list = json.load(f"{self.path}/genre.json")

    def recommend(self, genre):
        if self.Genre_list.get(genre) == None:
            return
        url = f'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20220302&tg={self.Genre_list[genre]}'
        url_res = requests.get(url)
        soup = bs(url_res.text,'html.parser')
        cinema = soup.select("#old_content > table > tbody > tr > td > div.tit5 > a")
        cinema_list = []
        for i in cinema:
            cinema_list.append(i.get_text())
        return {'cinema' : cinema_list}