import pickle
import requests
from pprint import pprint
from django.http import JsonResponse

from django.shortcuts import render
from sklearn.model_selection import train_test_split
from decouple import config

from common.interface.res_interface import QuickRepliesAndCarouselOutput, TextAndCarouselOutput, basicOutput, quickReplies
from common.movie_info import MovieAPI
from common.recommend.recommender import Recommender
from common.recommend.train import NEW_MF

from common.utils import byte2json, create_response_movie_info
from common.recommend.save_user import DataSave

"""/recommender"""
def get_input_data(request):
    if request.method == 'POST':
        json_result = byte2json(request.body)
        query = json_result["action"]["params"]["movie_name"]

        """영화 선택"""
        movie = MovieAPI()

        _movie_list = movie.movie_info_naver(query)

        _movie_list = sorted(_movie_list, key=(lambda x: x['userRating']), reverse=True)

        item_card, quick_replies = [], []
        for mov in _movie_list:
            item_card.append(create_response_movie_info(mov))
            quick_replies.append(quickReplies(
                label=mov['title'],
                msgText=mov['title'],
                blockId="628c82da299dbd02ee7a8738" # 선택한 영화를 저장하기 위해 다른 블럭으로 넘김
            ))

        if len(item_card) == 0:
            text = [
                {
                    "simpleText": {
                        "text": f"{query}에 맞는 검색 결과가 없습니다.\n평점이 4점미만인 영화인 경우 검색 대상에서 제외됩니다."
                    }
                }
            ]
            
            return JsonResponse(basicOutput(text))
        
        return JsonResponse(QuickRepliesAndCarouselOutput("itemCard", item_card, quick_replies))

"""/recommender/su"""
def save_data(request):
    if request.method == 'POST':
        json_result = byte2json(request.body)

        ML_SERVER_HOST = config("ML_SERVER_HOST")
        requests.post(f'{ML_SERVER_HOST}/rec/', json=json_result)

        output = [
            {
                "simpleText": {
                    "text": "더 추가하시겠습니까?\n추가 입력을 원하시는 경우 '예'버튼을 눌러주세요."
                }
            },
        ]

        quick_replies = [
            quickReplies(
                action='block',
                label='예',
                msgText='예',
                blockId='628c583e055a574d7df55691'
            ),
            quickReplies(
                action='block',
                label='아니오',
                msgText='아니오',
                blockId='628c7a8a055a574d7df55d12'
            )
        ]

        return JsonResponse(basicOutput(output, quick_replies))

def train(request):
    json_result = byte2json(request.body)

    # ML_SERVER_HOST = config("ML_SERVER_HOST")
    # requests.post(f'{ML_SERVER_HOST}/rec/t', json=json_result)
    pprint(json_result)

    return JsonResponse({
        "success": True
    })

def start_recommend(request):
    if request.method == 'POST':
        json_result = byte2json(request.body)

        ML_SERVER_HOST = config("ML_SERVER_HOST")
        rec_result = requests.post(f'{ML_SERVER_HOST}/rec/start', json=json_result)
        m = byte2json(rec_result.content)

        if rec_result.status_code != 200:
            return JsonResponse(m)

        m = m['movie']
        m_api = MovieAPI()

        out_result = ""
        movie_items = []
        selected_data = set()

        for m_title in m:
            data = m_api.movie_info_naver(m_title, ml_filtering=True)
            if data is not None and len(movie_items) < 3:
                movie_items.append(data[0])
                selected_data.add(m_title)
            else:
                out_result += "\n" + m_title
            
            if len(movie_items) == 3:
                break

        filtered_data = list(set(m) - selected_data)[:7]

        text = "\n".join(filtered_data)
        text = f"상위 3개 데이터와 그 외 7개의 추천 결과입니다.\n{text}"

        movie_card = []

        for mov in movie_items:
            movie_card.append(create_response_movie_info(mov))

        return JsonResponse(TextAndCarouselOutput("itemCard", movie_card, text))