from . import views
from django.urls import path,re_path

urlpatterns =[

    re_path(r'^Word_Link.ht.*', views.Word_Link),
    path('Word_Link_Result.html', views.Word_Link_Result)
]