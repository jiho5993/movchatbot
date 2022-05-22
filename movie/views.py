import pandas as pd

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from pprint import pprint
from common.interface.res_interface import *

from common.movie_info import MovieAPI
from common.userrating_recommend import UserRating_Recommend

from common.utils import byte2json, create_movie_info

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

# 영화 정보 조회
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
            movie_card.append(create_movie_info(mov))

        return JsonResponse(carouselOutput("itemCard", movie_card))

# 장르 추천
def genre_recommend(request):
    pass

# 박스오피스 순위
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

# 현재상영작 리스트
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

# 개봉예정작 리스트
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

"""
특정 영화 상영 질문
is_show_movie : 상영 판별 결과 목록 반환 (api 요청이 여기서부터 시작되는 코드)
show_movie_info : 판별 결과중 상영중인 영화만 유저에게 응답, quick reply로 블록 연계
booking_movie : 블록 연계 후, 사용자가 선택한 영화 예매링크 제공
"""
def is_show_movie(req):
    json_result = byte2json(req.body)
    query = json_result["action"]["params"]["sys_movie_name"]

    movie = MovieAPI()

    _movie_list = movie.movie_info_naver(query)

    _now_playing = pd.read_csv('./staticfiles/now_playing_movie.csv')

    result = []

    for movie in _movie_list:
        is_find = _now_playing.loc[_now_playing['title'] == movie['title']]
        
        result.append((movie, is_find.shape[0] != 0))

    return result

def show_movie_info(request):
    if request.method == 'POST':
        ml = is_show_movie(request)

        item_card = []
        quick_replies = []

        for mov, is_show in ml:
            if is_show is False:
                continue
            
            item_card.append(create_movie_info(mov))
            quick_replies.append(quickReplies(
                label=mov['title'],
                msgText=mov['title'],
                blockId="627dfc9445b5fc310645ddda"
            ))
        
        if len(item_card) == 0:
            output = [
                {
                    "simpleText": {
                        "text": "현재 상영중인 영화가 없습니다."
                    }
                }
            ]

            return JsonResponse(basicOutput(output))

        return JsonResponse(QuickRepliesAndCarouselOutput("itemCard", item_card, quick_replies))

def booking_movie(request):
    if request.method == 'POST':
        json_result = byte2json(request.body)
        movie_name = json_result['userRequest']['utterance']

        _now_playing = pd.read_csv('./staticfiles/now_playing_movie.csv')

        movie_data = _now_playing.loc[_now_playing['title'] == movie_name]
        index = movie_data.index[0]

        btn_list = [
            {
                "action": "webLink",
                "label": "예약하러가기",
                "webLinkUrl": movie_data.loc[index, 'book']
            }
        ]

        basic_card = [
            basicCard(
                title=movie_name,
                desc="",
                img=movie_data.loc[index, 'img'],
                btnList=btn_list
            )
        ]

        return JsonResponse(TextAndCarouselOutput(
            type="basicCard",
            output=basic_card,
            text=f"{movie_name}을 선택하셨습니다. 예매하기 버튼을 눌러주세요."
        ))