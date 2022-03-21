import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from pprint import pprint
from common.interface.res_interface import carouselOutput, itemCard

from common.movie_info import MovieAPI
from common.userrating_recommend import UserRating_Recommend
from common.kakao_map import KakaoMap
from common.theater_info import Theater_Info

from common.utils import byte2json

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
            if mov['actor'] == "":
                actors = "배우 없음"
            else:
                actors = mov['actor'].split('|')[:2]
                actors = ", ".join(actors) + " 등"

            if mov['director'] == "":
                directors = "감독 없음"
            else:
                directors = mov['director'].split('|')[:2]
                directors = ", ".join(directors)

            itemList = [
                {
                    "title": "장르",
                    "description": mov['genre']
                },
                {
                    "title": "국가",
                    "description": ("국가 없음" if mov['nation'] == None else mov['nation'])
                },
                {
                    "title": "러닝 타임",
                    "description": mov["playtime"]
                },
                {
                    "title": "감독 • 배우",
                    "description": directors + " | " + actors
                },
                {
                    "title": "등급",
                    "description": ("연령 등급 없음" if mov['age'] == None else mov['age'])
                }
            ]

            btnList = [
                {
                    "action": "webLink",
                    "label": "상세 정보 주소",
                    "webLinkUrl": mov['link']
                }
            ]

            movie_card.append(itemCard(
                title=mov['title'],
                desc="⭐ " + str(mov['userRating']),
                img=mov['image'],
                itemList=itemList,
                btnList=btnList
            ))

        return JsonResponse(carouselOutput("itemCard", movie_card))