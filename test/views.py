import json

from django.http import JsonResponse
from django.shortcuts import render
from common.interface.res_interface import basicOutput

from common.utils import byte2json
from pprint import pprint

# Create your views here.
def request_check(request):
    if request.method == 'POST':
        json_result = byte2json(request.body)

        pprint(json_result)

        return JsonResponse(basicOutput([
            {
                "simpleText": {
                    "text": json.dumps(json_result)
                }
            }
        ]))