from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    print(request)

    return JsonResponse(
        {
            "success": True,
            "message": "rest api 서버 테스트 성공",
            "response": None
        }
    )