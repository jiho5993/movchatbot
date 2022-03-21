import re

from pprint import pprint

from decouple import config
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from common.theater_info import Theater_Info
from common.kakao_map import KakaoMap

from common.utils import byte2json
from common.interface.res_interface import *

def theater_pos(request):
    json_result = byte2json(request.body)

    loc1 = json_result['action']['params']['sys_location1']
    loc2 = json_result['action']['params']['sys_location']

    loc = loc1 + " " + loc2

    map_api = KakaoMap()

    if request.method == 'POST':
        addr_info = map_api.addr_conv_pos(loc)['documents']

        card_list = []

        for info in addr_info:
            btnList = [
                {
                    "action": "message",
                    "label": "예매하기",
                    "messageText": "예매완료"
                },
                {
                    "action": "message",
                    "label": "영화/예매 이벤트",
                    "messageText": "이벤트는 없습니다~"
                },
                {
                    "action": "webLink",
                    "label": "가는길 찾기",
                    "webLinkUrl": info['place_url']
                }
            ]
            card_list.append(basicCard(
                title=info['place_name'],
                desc=info['road_address_name'],
                img="http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg",
                btnList=btnList
            ))

        return JsonResponse(carouselOutput("basicCard", card_list))