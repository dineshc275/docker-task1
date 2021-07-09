from django.urls import path

from app1 import views

urlpatterns = [
    path('data1/', views.DataAPI.as_view()),
]
