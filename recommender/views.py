import pickle
from django.http import JsonResponse

from django.shortcuts import render
from sklearn.model_selection import train_test_split
from common.interface.res_interface import QuickRepliesAndCarouselOutput, basicOutput, quickReplies
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

def train(request):
    path = './recommender/data'

    with open(f"{path}/datas.pickle", "rb") as f:
        df = pickle.load(f)

    ratings = df[['UserID', 'MovieID', "Rating"]]

    ratings.columns = ['user_id', 'movie_id', 'rating']

    R_temp = ratings.astype(int).pivot(index='user_id', columns='movie_id', values='rating').fillna(0)
    ratings_train, ratings_test = train_test_split(ratings.astype(int),
												test_size=0.2,
												shuffle=True,
												random_state=2021)

    hyper_params = {
        'K' : 30, # 이게 너무 크면 과적합
        'alpha' : 0.001,
        'beta' : 0.02,
        'iterations' : 30, # 이것도 과적합 가능성
        'verbose' : False
    }

    mf = NEW_MF(R_temp, hyper_params)
    mf.set_test(ratings_test)
    mf.test()

    with open(f"{path}/model.pickle", "wb") as f:
        pickle.dump(mf.full_prediction(), f)

    return JsonResponse({
        "success": True
    })

def start_recommend(request):
    if request.method == 'POST':
        json_result = byte2json(request.body)
        rc = Recommender(json_result)

        if rc.isUser is True:
            g = rc.genre_extract()
            m = rc.recommender_movie(10)

            # print("============================================================")
            # print(g)
            # print(m)
            # print("============================================================")

            result = ', '.join(m)

            result = f"추천 결과입니다.\n{result}"

            text = [
                {
                    "simpleText": {
                        "text": result
                    }
                },
            ]

            return JsonResponse(basicOutput(text))
        else:
            text = [
                {
                    "simpleText": {
                        "text": "추천을 받기 위한 등록된 데이터가 없습니다.\n데이터 추가 후 이용해주시기 바랍니다."
                    }
                },
            ]

            return JsonResponse(basicOutput(text))