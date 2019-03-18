from . import views
from django.urls import path

urlpatterns =[
    path('Word_Link.html', views.Word_Link),
    path('Word_Link_Result.html', views.Word_Link_Result)

]