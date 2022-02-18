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

        self.KOFIC_KEY = config("KOFIC_KEY")

        self.NUM_CORES = 2

    def get_naver(self, name, year):
        if year == '':
            return False

        name = re.sub("&", '', name)
        _url = f"https://openapi.naver.com/v1/search/movie.json?query={name}&yearfrom={year}&yearto={year}"
        _header = {
            "X-Naver-Client-Id": self.NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": self.NAVER_CLIENT_SECRET
        }

        res = requests.get(_url, headers=_header).json()

        # print("2 -----------------------------------")
        # print(_url)
        # pprint(res)

        if res['items'] == []:
            return False

        movie = res['items'][0]

        del movie["title"]
        del movie["subtitle"]
        del movie["pubDate"]

        return movie

    def thread_for_crawling(self, data):
        movieNm = data["movieNm"]
        year = data["prdtYear"]
        # print("1 -----------------------------------")
        # pprint(data)
        result = self.get_naver(movieNm, year)

        if result is False:
            return {
                "isSuccess": False,
                "userRating": "0.00"
            }

        movieCd = data["movieCd"]
        _kofic_url = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={self.KOFIC_KEY}&movieCd={movieCd}"

        res = requests.get(_kofic_url).json()
        movie_detail = res["movieInfoResult"]["movieInfo"]

        age = ""
        if movie_detail["audits"] == []:
            age = "전체 이용가"
        else:
            age = movie_detail["audits"][0]["watchGradeNm"]

        outline_dict = dict(
            title=movieNm,
            isSuccess=True,
            genre=data["genreAlt"],
            nation=data["repNationNm"],
            playtime=movie_detail["showTm"] + "분",
            pubDate=movie_detail["openDt"],
            age=age
        )
        result.update(outline_dict)

        return result

    def movie_list(self, movieNm):
        _url = f"https://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={self.KOFIC_KEY}&movieNm={movieNm}"

        res = requests.get(_url)

        if res.status_code == 200:
            data = res.json()["movieListResult"]["movieList"]

            pool = Pool(self.NUM_CORES)

            result = pool.map(self.thread_for_crawling, data)

            pool.close()
            pool.join()

            return result
        else:
            print ('Error : {}'.format(res.status_code))
            return False

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
        result = movie.movie_list(query)

        if result == False:
            return JsonResponse(
                {
                    "success": False
                }
            )

        # pprint(result)

        result = sorted(result, key=(lambda x: x['userRating']), reverse=True)
        movie_card = []

        for mov in result:
            if mov["isSuccess"] is False:
                continue

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