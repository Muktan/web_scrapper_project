from . import views
from django.urls import path

urlpatterns =[
    path('index.html', views.index)
]