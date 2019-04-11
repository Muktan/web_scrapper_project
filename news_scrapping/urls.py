from django.urls import path,re_path
from django.contrib import admin
from news_scrapping import views

urlpatterns =[
    re_path(r'^news_result.*', views.news_result),
]