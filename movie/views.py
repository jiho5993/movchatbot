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
        data['userRating'] = float(data['userRating'])

        # 평점이 5.0 미만인 영화는 잘라버림
        if data['userRating'] < 5.0:
            return

        data['title'] = re.sub('<b>|</b>', '', data['title']) # 영화 제목에 들어간 <b> </b> 태그 제거

        movie_link = data['link']
        code = movie_link.split("=")[-1]
        
        review = f'https://movie.naver.com/movie/bi/mi/point.naver?code={code}'

        url_res = requests.get(movie_link)
        soup = bs(url_res.text,'html.parser')

        # global new_info
        new_info = soup.select("dl.info_spec")[0]

        is_span = new_info.find_all("span")
        
        playtime, genre, nation, pubDate_info = None, [], None, []

        for i in is_span:
            filtered = i.select("a")

            if filtered == [] and playtime == None: # playtime
                playtime = i.get_text().strip()
            else: # genre / nation / pubDate_info
                for info in filtered:
                    p = re.compile("genre|nation|open")
                    state = p.findall(info['href'])

                    if len(state) == 0:
                        continue

                    text = info.get_text().strip()
                    
                    if state[0] == "genre":
                        genre.append(text)
                    elif state[0] == "nation":
                        nation = text
                    else:
                        pubDate_info.append(text)

        genre = ",".join(genre)
        if genre == "":
            genre = None

        pubDate_info = "".join(pubDate_info)
        if pubDate_info == "":
            pubDate_info = None

        age = soup.select("#content > div.article > div.mv_info_area > div:nth-of-type(1) > dl.info_spec > dd > p > a")
        age_info = None
        for ages in age:
            if ages['href'].find('grade') != -1:
                age_info = ages.get_text()
                break

        outline_dict = dict(
            review=review,
            genre=genre,
            nation=nation,
            playtime=playtime,
            pubDate_info=pubDate_info,
            age=age_info
        )
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

            # 평점에서 걸러진 데이터 필터링
            cnt = 0
            for i in range(len(result)):
                if result[i - cnt] is None:
                    del result[i - cnt]
                    cnt += 1

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
        # result = movie.movie_info_naver(query)

        # if result == False:
        #     return JsonResponse(
        #         {
        #             "success": False
        #         }
        #     )

        # result = sorted(result, key=(lambda x: x['userRating']), reverse=True)
        # movie_card = []

        # for mov in result:
        #     # if mov["isSuccess"] is False:
        #     #     continue

        #     actors = mov['actor'].split('|')[:2]
        #     actors = ", ".join(actors) + " 등"

        #     directors = mov['director'].split('|')[:2]
        #     directors = ", ".join(directors)

        #     description = "⭐ " + str(mov['userRating']) + "\n" \
        #         + "· 개요 " + ("장르 없음" if mov['genre'] == None else mov['genre']) + " | " \
        #         + ("국가 없음" if mov['nation'] == None else mov['nation']) + " | " \
        #         + ("러닝타임 없음" if mov["playtime"] == None else mov["playtime"]) + "\n" \
        #         + "· 감독 " + directors + "\n" \
        #         + "· 출연 " + actors + "\n" \
        #         + "· 등급 " + ("연령 등급 없음" if mov['age'] == None else mov['age'])

        #     movie_card.append(
        #         {
        #             "title": mov['title'],
        #             "description": description,
        #             "thumbnail": {
        #                 "imageUrl": mov['image']
        #             },
        #             "buttons": [
        #                 {
        #                     "action": "webLink",
        #                     "label": "상세 정보 주소",
        #                     "webLinkUrl": mov['link']
        #                 }
        #             ]
        #         }
        #     )

        return JsonResponse(
            {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "itemCard": {
                                "thumbnail": {
                                    "imageUrl": "https://w.namu.la/s/45507892b4f48b2b3d4a6386f6dae20c28376a8ef5dfb68c7cc95249ec358e3e68df77594766021173b2e6acf374b79ce02e9eeef61fcdf316659e30289e123fbddf6e5ec3492eddbc582ee5a59a2ff5d6ee84f57ad19277d179b613614364ad",
                                    "width": 800,
                                    "height": 400
                                },
                                "profile": {
                                    "title": "AA Airline"
                                },
                                "itemList": [
                                    {
                                        "title": "Flight",
                                        "description": "KE0605"
                                    }
                                ],
                                "title": "test",
                                "description": "test",
                                "itemListAlignment" : "right",
                                "itemListSummary": {
                                    "title": "Total",
                                    "description": "$4,032.54"
                                },
                                "buttons": [
                                    {
                                        "label": "View Boarding Pass",
                                        "action": "webLink",
                                        "webLinkUrl": "https://namu.wiki/w/%EB%82%98%EC%97%B0(TWICE)"
                                    }
                                ],
                                "buttonLayout" : "vertical"
                            }
                        }
                    ]
                }
            }
        )