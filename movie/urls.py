from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie-info', views.movie_info),
    path('genre', views.genre_recommend),
    path('box-office', views.box_office_rank),
    path('now-playing', views.now_playing),
    path('upcoming', views.upcoming_movie)
]