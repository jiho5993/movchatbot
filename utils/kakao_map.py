import urllib.request as req
import requests

from decouple import config

class KakaoMap:
    def __init__(self):
        self.KAKAO_MAP_API_KEY = config("KAKAO_MAP_API_KEY")

    def addr_conv_pos(self, addr):
        _kakao_url = f'https://dapi.kakao.com/v2/local/search/address.json?analyze_type=similar&page=1&size=1&query={addr}'
        _kakao_header = {
            'Authorization': self.KAKAO_MAP_API_KEY
        }
        res = requests.get(_kakao_url, headers=_kakao_header)

        if res.status_code == 200:
            if len(res.json()['documents']) == 0:
                return self.pos_conv_addr(addr, None, None, None, None)
            else:
                return res.json()
        else:
            print('Error : {}'.format(res.status_code))
            return '에러가 발생하였습니다.'

    def pos_conv_addr(self, query, x, y, radius, error=0):
        if error == None:
            _kakao_url = f'https://dapi.kakao.com/v2/local/search/keyword.json?page=1&sort=accuracy&query={query}'
        else:
            _kakao_url = f'https://dapi.kakao.com/v2/local/search/keyword.json?page=1&sort=accuracy&query={query}&size=15&x={x}&y={y}&radius={radius}&category_group_code=CT1'
        _kakao_header = {
            'Authorization': self.KAKAO_MAP_API_KEY
        }
        res = requests.get(_kakao_url, headers=_kakao_header)

        if res.status_code == 200:
            return res.json()
        else:
            print('Error : {}'.format(res.status_code))
            return '에러가 발생하였습니다.'