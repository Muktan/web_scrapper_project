from . import views
from django.urls import path,re_path

urlpatterns =[

    re_path(r'^Word_Link.html.*', views.Word_Link),
    path('Word_Link_Result.html', views.Word_Link_Result)
]