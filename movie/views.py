from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from pprint import pprint
from common.interface.res_interface import TextAndCarouselOutput, basicCard, carouselOutput, itemCard

from common.movie_info import MovieAPI
from common.userrating_recommend import UserRating_Recommend

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
                },
                status=status.HTTP_400_BAD_REQUEST
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

def genre_recommend(request):
    pass

def box_office_rank(request):
    if request.method == 'POST':
        bo = MovieAPI()

        bo = bo.createBoxOfficeList()

        card_list = []
        for i, item in enumerate(bo):
            title = item['title']
            rank = str(i + 1) + "위"
            img = item['thumb']

            card = basicCard(title, rank, img, None)
            del card['buttons']

            card_list.append(card)

        return JsonResponse(carouselOutput("basicCard", card_list))

def now_playing(request):
    if request.method == 'POST':
        np = MovieAPI()

        """
        TODO: get order option
        open (개봉)
        point (참여, 평점)
        """
        order = 'open'

        np = np.createNowPlaying(order)

        item_card = []
        for item in np:
            item_list = [
                {
                    "title": "개봉일",
                    "description": item['date']
                },
                {
                    "title": "등급",
                    "description": ("연령 등급 없음" if item['age'] == None else item['age'])
                },
                {
                    "title": "평점 • 참여수",
                    "description": "⭐ " + str(item['star']) + " | " + str(item['man']) + "명"
                }
            ]

            item_card.append(itemCard(
                title=item['title'],
                desc="",
                img=item['img'],
                itemList=item_list,
                btnList=[
                    {
                        "label":  "영화 상세 정보",
                        "action": "webLink",
                        "webLinkUrl": item['link']
                    }
                ]
            ))

        return JsonResponse(TextAndCarouselOutput("itemCard", item_card, f"{order}순으로 정렬된 목록입니다."))

def upcoming_movie(request):
    if request.method == 'POST':
        # 이번 달, 다음 달 개봉일 영화를 데이터로 기대지수순으로 정렬한 데이터를 가져온다.
        um = MovieAPI()
        um = um.createUpcomingMovie()

        item_card = []
        for movie in um:
            item_list = [
                {
                    "title": "개봉일",
                    "description": movie['open_dt']
                },
                {
                    "title": "등급",
                    "description": movie['age']
                },
                {
                    "title": "좋아요 • 싫어요",
                    "description": str(movie['star'][0]) + " • " + str(movie['star'][1])
                }
            ]

            item_card.append(itemCard(
                title=movie['title'],
                desc='',
                img=movie['img'],
                itemList=item_list,
                btnList=[
                    {
                        "label":  "영화 상세 정보",
                        "action": "webLink",
                        "webLinkUrl": movie['link']
                    }
                ]
            ))
        return JsonResponse(TextAndCarouselOutput("itemCard", item_card, f"이번 달, 다음 달 개봉일 영화를 기대지수순으로 정렬한 목록입니다."))