import pandas as pd

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from pprint import pprint
from common.interface.res_interface import *

from common.movie_info import MovieAPI
from common.genre_recommender import GenreRecommender

from common.utils import *

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
            movie_card.append(create_response_movie_info(mov))

        if len(movie_card) == 0:
            text = [
                {
                    "simpleText": {
                        "text": f"{query}에 맞는 검색 결과가 없습니다.\n평점이 4점미만인 영화인 경우 검색 대상에서 제외됩니다."
                    }
                }
            ]
            
            return JsonResponse(basicOutput(text))

        return JsonResponse(carouselOutput("itemCard", movie_card))

# 장르 추천
def genre_recommend(request):
    if request.method == 'POST':
        json_result = byte2json(request.body)
        type = json_result['action']['params']['Genre']

        gr = GenreRecommender(type)
        rec_list = gr.recommend()

        item_card = []

        for item in rec_list:
            if len(item_card) == 5:
                break

            movie_info = get_movie_info(item['link'], get_img=True)
            if movie_info is None:
                continue

            genre = movie_info['genre']
            nation = movie_info['nation']
            age_info = movie_info['age_info']
            img = movie_info['img']

            item_list = [
                {
                    "title": "장르",
                    "description": genre
                },
                {
                    "title": "국가",
                    "description": ("국가 없음" if nation == None else nation)
                },
                {
                    "title": "등급",
                    "description": ("연령 등급 없음" if age_info == None else age_info)
                }
            ]

            btn_list = [
                {
                    "action": "webLink",
                    "label": "상세 정보 주소",
                    "webLinkUrl": item['link']
                }
            ]

            item_card.append(itemCard(
                title=item['title'],
                desc="",
                img=img,
                itemList=item_list,
                btnList=btn_list
            ))

        return JsonResponse(TextAndCarouselOutput(
            type='itemCard',
            output=item_card,
            text=f'{type}(으)로 조회한 결과입니다.\n' \
                '개봉전 영화도 포함되어 있을 수도 있습니다.\n' \
                '더보기를 원하시는 경우 아래의 링크를 클릭해주세요.\n' \
                f'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cnt&date={gr.date}&tg={gr.genre_index}'
        ))

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
        json_result = byte2json(request.body)
        np = MovieAPI()

        order = json_result['action']['params']['now_playing_order_option']

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

        if order == 'open':
            order = '개봉'
        else:
            order = '평점, 참여'

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
            
            item_card.append(create_response_movie_info(mov))
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
            text=f"{movie_name}을 선택하셨습니다.\n예매를 원하시는 경우, 예매하기 버튼을 눌러주세요."
        ))