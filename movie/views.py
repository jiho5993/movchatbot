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

from classes.movie_info import MovieAPI
from classes.userrating_recommend import UserRating_Recommend
from classes.kakao_map import KakaoMap
from classes.theater_info import Theater_Info

def byte2json(body):
    decoded = body.decode('utf-8')
    return json.loads(decoded)

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
        #         + ("장르 없음" if mov['genre'] == None else mov['genre'])
        #         # + ("국가 없음" if mov['nation'] == None else mov['nation']) + " | " \
        #         # + ("러닝타임 없음" if mov["playtime"] == None else mov["playtime"]) + "\n" \
        #         # + "· 감독 " + directors + "\n" \
        #         # + "· 출연 " + actors + "\n" \
        #         # + "· 등급 " + ("연령 등급 없음" if mov['age'] == None else mov['age'])

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
        #                 },
        #                 {
        #                     "action": ""
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
                            "carousel": {
                                "type": "itemCard",
                                "items": [
                                    {
                                        "thumbnail": {
                                            "imageUrl": "https://w.namu.la/s/45507892b4f48b2b3d4a6386f6dae20c28376a8ef5dfb68c7cc95249ec358e3e68df77594766021173b2e6acf374b79ce02e9eeef61fcdf316659e30289e123fbddf6e5ec3492eddbc582ee5a59a2ff5d6ee84f57ad19277d179b613614364ad",
                                            "width": 800,
                                            "height": 400
                                        },
                                        "profile": {
                                            "title": "test profile 1"
                                        },
                                        "itemList": [
                                            {
                                                "title": "1",
                                                "description": "desc"
                                            },
                                            {
                                                "title": "2",
                                                "description": "desc 2"
                                            }
                                        ]
                                    },
                                    {
                                        "thumbnail": {
                                            "imageUrl": "https://w.namu.la/s/45507892b4f48b2b3d4a6386f6dae20c28376a8ef5dfb68c7cc95249ec358e3e68df77594766021173b2e6acf374b79ce02e9eeef61fcdf316659e30289e123fbddf6e5ec3492eddbc582ee5a59a2ff5d6ee84f57ad19277d179b613614364ad",
                                            "width": 800,
                                            "height": 400
                                        },
                                        "profile": {
                                            "title": "test profile 2"
                                        },
                                        "itemList": [
                                            {
                                                "title": "1",
                                                "description": "desc"
                                            },
                                            {
                                                "title": "2",
                                                "description": "desc 2"
                                            }
                                        ]
                                    },
                                    {
                                        "thumbnail": {
                                            "imageUrl": "https://w.namu.la/s/45507892b4f48b2b3d4a6386f6dae20c28376a8ef5dfb68c7cc95249ec358e3e68df77594766021173b2e6acf374b79ce02e9eeef61fcdf316659e30289e123fbddf6e5ec3492eddbc582ee5a59a2ff5d6ee84f57ad19277d179b613614364ad",
                                            "width": 800,
                                            "height": 400
                                        },
                                        "profile": {
                                            "title": "test profile 3"
                                        },
                                        "itemList": [
                                            {
                                                "title": "1",
                                                "description": "desc"
                                            },
                                            {
                                                "title": "2",
                                                "description": "desc 2"
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        )