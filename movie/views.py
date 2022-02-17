import requests
import json
import re

import multiprocessing as mp
from multiprocessing import Pool

from bs4 import BeautifulSoup as bs
from decouple import config
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from pprint import pprint

def byte2json(body):
    decoded = body.decode('utf-8')
    return json.loads(decoded)

class MovieAPI:
    def __init__(self):
        self.NAVER_CLIENT_ID = config("NAVER_CLIENT_ID")
        self.NAVER_CLIENT_SECRET = config("NAVER_CLIENT_SECRET")
        self.NUM_CORES = 4

    def thread_for_crawling(self, data):
        data['title'] = re.sub('<b>|</b>', '', data['title']) # 영화 제목에 들어간 <b> </b> 제거
        code = data['link'].split("=")[1]
        
        review = f'https://movie.naver.com/movie/bi/mi/point.naver?code={code}'

        url = f'https://movie.naver.com/movie/bi/mi/basic.naver?code={code}'
        url_res = requests.get(url)
        soup = bs(url_res.text,'html.parser')
        genre = soup.select("#content > div.article > div.mv_info_area > div:nth-of-type(1) > dl.info_spec > dd > p > span")

        genre_info = re.sub(' |\n|\r|\t', '', genre[0].get_text().strip())
        nation = re.sub(' |\n|\r|\t', '', genre[1].get_text().strip())
        playtime = re.sub(' |\n|\r|\t', '', genre[2].get_text().strip())

        if len(genre) > 3:
            pubDate_info = re.sub(' |\n|\r|\t', '', genre[-1].get_text().strip())
        else:
            pubDate_info = None

        age = soup.select("#content > div.article > div.mv_info_area > div:nth-of-type(1) > dl.info_spec > dd > p > a")
        age_info = None
        for ages in age:
            if ages['href'].find('grade') != -1:
                age_info = ages.get_text()
                break

        outline_dict = dict(review=review, genre=genre_info, nation=nation, playtime=playtime, pubDate_info=pubDate_info, age=age_info)
        data.update(outline_dict)

        return data

    def movie_info_naver(self, name):
        _url = f"https://openapi.naver.com/v1/search/movie.json?query={name}&display=20"
        _header = {
            "X-Naver-Client-Id": self.NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": self.NAVER_CLIENT_SECRET
        }

        res = requests.get(_url, headers=_header)

        if res.status_code == 200:
            data = res.json()

            pool = Pool(self.NUM_CORES)

            result = pool.map(self.thread_for_crawling, data['items'])

            pool.close()
            pool.join()

            return result
        else:
            print ('Error : {}'.format(res.status_code))
            return '에러가 발생하였습니다.'

# Create your views here.
def index(request):
    if request.method == "POST":
        return JsonResponse(
            {
                "success": True,
                "message": "rest api 서버 테스트 성공",
                "response": None
            }
        )

def movie_info(request):
    json_result = byte2json(request.body)
    query = json_result["action"]["params"]["sys_movie_name"]

    movie = MovieAPI()

    if request.method == 'POST':
        result = movie.movie_info_naver(query)

        if result == False:
            return JsonResponse(
                {
                    "success": False
                }
            )

        result = sorted(result, key=(lambda x: x['userRating']), reverse=True)
        movie_card = []

        for mov in result:
            actors = mov['actor'].split('|')[:2]
            actors = ", ".join(actors) + " 등"

            directors = mov['director'].split('|')[:2]
            directors = ", ".join(directors)

            description = "⭐ " + mov['userRating'] + "\n" \
                + "· 개요 " + mov['genre'] + " | " + mov['nation'] + " | " + mov["playtime"] + "\n" \
                + "· 감독 " + directors + "\n" \
                + "· 출연 " + actors + "\n" \
                + "· 등급 " + ("연령 등급 없음" if mov['age'] == None else mov['age'])

            movie_card.append(
                {
                    "title": mov['title'],
                    "description": description,
                    "thumbnail": {
                        "imageUrl": mov['image']
                    },
                    "buttons": [
                        {
                            "action": "webLink",
                            "label": "상세 정보 주소",
                            "webLinkUrl": mov['link']
                        },
                        {
                            "action": "webLink",
                            "label": "평점",
                            "webLinkUrl": mov['review']
                        }
                    ]
                }
            )

        return JsonResponse(
            {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "carousel": {
                                "type": "basicCard",
                                "items": movie_card
                            }
                        }
                    ]
                }
            }
        )