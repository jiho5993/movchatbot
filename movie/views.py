import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decouple import config

# Create your views here.
def index(request):
    NAVER_CLIENT_ID = config("NAVER_CLIENT_ID")
    NAVER_CLIENT_SECRET = config("NAVER_CLIENT_SECRET")

    print(NAVER_CLIENT_ID)

    if request.method == "POST":
        return JsonResponse(
            {
                "success": True,
                "message": "rest api 서버 테스트 성공",
                "response": None
            }
        )