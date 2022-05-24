import pickle
from django.http import JsonResponse

from django.shortcuts import render
from common.interface.res_interface import QuickRepliesAndCarouselOutput, basicOutput, quickReplies
from common.movie_info import MovieAPI

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

        ds = DataSave(json_result)
        new_data = ds.save_data()

        new_user_dataset = new_data[0]
        new_movie_dataset = new_data[1]

        path = './recommender/data'

        with open(f'{path}/users.pickle', 'wb') as f:
            pickle.dump(new_user_dataset, f)

        with open(f'{path}/datas.pickle', 'wb') as f:
            pickle.dump(new_movie_dataset, f)

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
                blockId='628c799793b31d5b60ab62fc'
            ),
            quickReplies(
                action='block',
                label='아니오',
                msgText='아니오',
                blockId='628c7a8a055a574d7df55d12'
            )
        ]

        return JsonResponse(basicOutput(output, quick_replies))

def train():
    return

def rec(request):
    # test = user_recommender()
    return """추천"""