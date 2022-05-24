from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_input_data),
    path('su', views.save_data)
]