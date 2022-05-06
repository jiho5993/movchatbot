import requests
import re

import multiprocessing as mp
from multiprocessing import Pool
from datetime import datetime

from bs4 import BeautifulSoup as bs
from decouple import config

from pprint import pprint

class MovieAPI:
    def __init__(self):
        self.NAVER_CLIENT_ID = config("NAVER_CLIENT_ID")
        self.NAVER_CLIENT_SECRET = config("NAVER_CLIENT_SECRET")
        self.NUM_CORES = 4

    def thread_for_crawling(self, data):
        data['userRating'] = float(data['userRating'])

        # 기저 사례 처리
        # 평점이 5.0 미만이거나 이미지가 없으면 잘라버림
        if data['userRating'] < 5.0 or data['image'] == "":
            return

        data['title'] = re.sub('<b>|</b>', '', data['title']) # 영화 제목에 들어간 <b> </b> 태그 제거

        movie_link = data['link']
        code = movie_link.split("=")[-1]
        
        review = f'https://movie.naver.com/movie/bi/mi/point.naver?code={code}'

        url_res = requests.get(movie_link)
        soup = bs(url_res.text,'html.parser')

        # global new_info
        new_info = soup.select("dl.info_spec")[0]

        is_span = new_info.find_all("span")
        
        playtime, genre, nation, pubDate_info = None, [], None, []

        for i in is_span:
            filtered = i.select("a")

            if filtered == [] and playtime == None: # playtime
                playtime = i.get_text().strip()
            else: # genre / nation / pubDate_info
                for info in filtered:
                    p = re.compile("genre|nation|open")
                    state = p.findall(info['href'])

                    if len(state) == 0:
                        continue

                    text = info.get_text().strip()
                    
                    if state[0] == "genre":
                        genre.append(text)
                    elif state[0] == "nation":
                        if nation is not None:
                            nation += ", " + text
                        else:
                            nation = text
                    else:
                        pubDate_info.append(text)

        genre = ",".join(genre)
        # 보여줄 장르나 러닝 타임이 없으면 영화 잘라버림
        if genre == "" or playtime is None:
            return

        pubDate_info = "".join(pubDate_info)
        if pubDate_info == "":
            pubDate_info = None

        age = soup.select("#content > div.article > div.mv_info_area > div:nth-of-type(1) > dl.info_spec > dd > p > a")
        age_info = None
        for ages in age:
            if ages['href'].find('grade') != -1:
                age_info = ages.get_text()
                break

        outline_dict = dict(
            review=review,
            genre=genre,
            nation=nation,
            playtime=playtime,
            pubDate_info=pubDate_info,
            age=age_info
        )
        data.update(outline_dict)

        return data

    def movie_info_naver(self, name):
        _url = f"https://openapi.naver.com/v1/search/movie.json?query={name}&display=20"
        _header = {
            "X-Naver-Client-Id": self.NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": self.NAVER_CLIENT_SECRET
        }

        res = requests.get(_url, headers=_header)

        if res.status_code == 200:
            data = res.json()

            pool = Pool(self.NUM_CORES)

            result = pool.map(self.thread_for_crawling, data['items'])

            pool.close()
            pool.join()

            # 평점에서 걸러진 데이터 필터링
            cnt = 0
            for i in range(len(result)):
                if result[i - cnt] is None:
                    del result[i - cnt]
                    cnt += 1

            return result
        else:
            print ('Error : {}'.format(res.status_code))
            return '에러가 발생하였습니다.'

    def __getBoxOfficeInfo(self):
        _url = "https://search.naver.com/search.naver?where=nexearch&query=박스오피스순위"
        html = requests.get(_url)
        soup = bs(html.text, 'html.parser')
        
        res = soup.select("div._panel_popular > div.list_image_info > div.list_image_box > ul._panel")
        return res[0] # index 0 is popular panel
    
    def createBoxOfficeList(self):
        result = []
        data = self.__getBoxOfficeInfo()

        is_li = data.select("li")

        for i in range(10):
            img = is_li[i].select("img")[0]

            title = img["alt"]
            thumb = img["src"]
            
            result.append(
                dict(
                    title=title,
                    thumb=thumb
                )
            )
        
        return result

    def __getNowPlaying(self):
        _url = "https://movie.naver.com/movie/running/current.naver?view=list&tab=normal&order=open"
        html = requests.get(_url)
        soup = bs(html.text, 'html.parser')
        
        res = soup.select("#content > div.article > div > div.lst_wrap > ul > li")
        return res

    def createNowPlaying(self, order='open'):
        res = []

        movie_list = self.__getNowPlaying()

        now = datetime.now()

        for i in movie_list:
            try:
                # date
                date = i.select_one("dl.info_txt1 > dd")
                date = date.text.split("|")
                date = re.sub(' |\r|\n|\t|개봉|[.]', '', date[2])

                open_date = datetime.strptime(date, "%Y%m%d")

                date_diff = now - open_date

                if date_diff.days > 15:
                    break

                # age
                age = i.select_one("dt.tit > span")
                if age is not None:
                    age = age.text

                # title
                title = i.select_one("dt.tit > a").text

                # img, link
                img = i.select_one("div.thumb > a > img")
                link = i.select_one("div.thumb > a")

                # star point
                star = i.select_one("dl.lst_dsc > dd.star > dl.info_star > dd > div.star_t1 > a > span.num")
                star = float(star.text)

                pointing_man = i.select_one("dl.lst_dsc > dd.star > dl.info_star > dd > div.star_t1 > a > span.num2 > em")
                pointing_man = int(re.sub(',', '', pointing_man.text))

                res.append(dict(
                    age = age,
                    title = title,
                    date = date,
                    img = img["src"],
                    link = f"https://movie.naver.com{link['href']}",
                    star = star,
                    man = pointing_man
                ))
            except:
                print(f"this is error ----------- {i}")

        # 정렬 기준
        if order == 'open':
            pass
        elif order == 'point':
            res = sorted(res, key=(lambda x: (x['man'], x['star'])), reverse=True)

        return res