import requests

from bs4 import BeautifulSoup as bs
from decouple import config

class MovieAPI:
    def __init__(self):
        self.NAVER_CLIENT_ID = config("NAVER_CLIENT_ID")
        self.NAVER_CLIENT_SECRET = config("NAVER_CLIENT_SECRET")

    def movie_info_naver(self, name, genre, country):
        _url = f"https://openapi.naver.com/v1/search/movie.json?query={name}&display=20&genre={genre}&country={country}"
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
                review_list = []
                data['items'][i]['title'] = data['items'][i]['title'].replace('<b>','').replace('</b>','') # 영화 제목에 들어간 <b> </b> 제거
                reversed_str = data['items'][i]['link'][::-1] # 링크에서 코드 뽑아오기 위함
                code = ''
                for j in reversed_str:
                    if j == '=':
                        break;
                    code = j + code
                
                # 줄거리 크롤링 코드, 줄거리가 없으면 줄거리 없음을 넣어줌
                url = f'https://movie.naver.com/movie/bi/mi/basic.naver?code={code}#'
                url_res = requests.get(url)
                soup = bs(url_res.text,'html.parser')
                summary = soup.select("#content > div.article > div.section_group.section_group_frst > div:nth-of-type(1) > div > div.story_area > p")
                if summary == []:
                    summary = '줄거리 없음.'
                else:
                    summary = summary[0].get_text().replace('\xa0','').replace('\r','') # 불필요한 단어들 제거
                summary_dict = {'summary' : f'{summary}'} # data['items'][i]에 있는 영화 정보는 dict형식, update 시켜주기위해 형식을 맞춰줌
                data['items'][i].update(summary_dict)

                # 리뷰 크롤링 코드
                url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code={code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1'
                html = requests.get(url)
                soup = bs(html.content,'html.parser')

                for j in range(10): # 리뷰를 첫 페이지 10개만 가져옴, 기본은 공감순으로 정렬되어있음
                    review = soup.find('span',{'id':f'_filtered_ment_{j}'})
                    review = review.get_text().strip()
                    review_list.append(review)
                review_dict = {'review': f'{review_list}'}
                data['items'][i].update(review_dict)
                
            return data['items']
        else:
            print ('Error : {}'.format(res.status_code))
            return '에러가 발생하였습니다.'