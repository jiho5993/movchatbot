from pprint import pprint

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from common.theater_info import Theater_Info

from common.utils import byte2json
from common.interface.res_interface import *

def theater_pos(request):
    json_result = byte2json(request.body)

    loc1 = json_result['action']['params']['sys_location1']

    try:
        loc2 = json_result['action']['params']['sys_location']
    except KeyError:
        loc2 = ""

    loc = loc1 + " " + loc2
    theater_type = json_result['action']['params']['theater']

    map_api = Theater_Info()

    if request.method == 'POST':
        theater_infos = map_api.theater(loc, theater_type)

        card_list = []

        for name in theater_infos.keys():
            theater = theater_infos[name]

            btnList = [
                {
                    "action": "webLink",
                    "label": "예매하기",
                    "webLinkUrl": theater['ticket']
                },
                {
                    "action": "webLink",
                    "label": "영화/예매 이벤트",
                    "webLinkUrl": theater['event']
                },
                {
                    "action": "webLink",
                    "label": "가는길 찾기",
                    "webLinkUrl": theater['nav']
                }
            ]
            card_list.append(basicCard(
                title=name,
                desc=theater['pos']['pos1'] + "\n" + theater['pos']['pos2'],
                img=theater['img'],
                btnList=btnList
            ))

        return JsonResponse(carouselOutput("basicCard", card_list))