from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_input_data),
    path('su', views.save_data),
    path('t', views.train),
    path('start', views.start_recommend)
]