import json

from common.interface.res_interface import itemCard

def byte2json(body):
    decoded = body.decode('utf-8')
    return json.loads(decoded)

def create_movie_info(mov):
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