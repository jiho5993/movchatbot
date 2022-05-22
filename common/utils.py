import json
import requests
import re

from bs4 import BeautifulSoup as bs

from common.interface.res_interface import itemCard

def byte2json(body):
    decoded = body.decode('utf-8')
    return json.loads(decoded)

def create_response_movie_info(mov):
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

    return itemCard(
        title=mov['title'],
        desc="⭐ " + str(mov['userRating']),
        img=mov['image'],
        itemList=itemList,
        btnList=btnList
    )

def get_movie_info(link, get_img=False):
    url_res = requests.get(link)
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

    img = ''
    if get_img is True:
        try:
            img = soup.select_one('div.poster > a > img')['src']
        except:
            pass

    # print("------", playtime, genre, nation, pubDate_info, age_info, img)

    return {
        'playtime': playtime,
        'genre': genre,
        'nation': nation,
        'pubDate_info': pubDate_info,
        'age_info': age_info,
        'img': img
    }