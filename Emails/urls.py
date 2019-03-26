from . import views
from django.urls import path

urlpatterns =[
    path('Emails.html', views.Emails),
    path('Emails_Result.html', views.Emails_Result),
    path('Emails_Downloads.html',views.Emails_Downloads),
]