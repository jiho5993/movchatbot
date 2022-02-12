import requests

from bs4 import BeautifulSoup as bs
from decouple import config
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class MovieAPI:
    def __init__(self):
        self.NAVER_CLIENT_ID = config("NAVER_CLIENT_ID")
        self.NAVER_CLIENT_SECRET = config("NAVER_CLIENT_SECRET")

    def movie_info_naver(self, name):
        _url = f"https://openapi.naver.com/v1/search/movie.json?query={name}&display=20"
        _header = {
            "X-Naver-Client-Id": self.NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": self.NAVER_CLIENT_SECRET
        }

        res = requests.get(_url, headers=_header)

        if res.status_code == 200:
            data = res.json()
            display = data['display']

            # 설정한 영화 숫자만큼 체크
            for i in range(display):
                data['items'][i]['title'] = data['items'][i]['title'].replace('<b>','').replace('</b>','') # 영화 제목에 들어간 <b> </b> 제거
                reversed_str = data['items'][i]['link'][::-1] # 링크에서 코드 뽑아오기 위함
                code = ''

                for j in reversed_str:
                    if j == '=':
                        break;
                    code = j + code

                review = {'review': f'https://movie.naver.com/movie/bi/mi/point.naver?code={code}'}
                data['items'][i].update(review)

            return data['items']
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
    print(request.body)

    movie = MovieAPI()

    if request.method == 'POST':
        # print(movie.movie_info_naver("아이언맨"))
        result = movie.movie_info_naver("아이언맨")

        if result == False:
            return JsonResponse(
                {
                    "success": False
                }
            )

        movie_card = []

        for mov in result:
            actors = mov['actor'].split('|')
            actors = actors[:2]
            actors = ", ".join(actors)

            movie_card.append(
                {
                    "title": mov['title'],
                    "description": "⭐ " + mov['userRating'] + " " + actors,
                    "thumbnail": {
                        "imageUrl": mov['image']
                    },
                    "buttons": [
                        {
                            "action": "webLink",
                            "label": "상세 정보 주소",
                            "webLinkUrl": mov['link']
                        },
                        {
                            "action": "webLink",
                            "label": "평점",
                            "webLinkUrl": mov['review']
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