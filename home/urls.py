from . import views
from django.urls import path

urlpatterns =[
    path('index.html', views.index),
    path('login.html', views.login),
    path('signup.html',views.signup),
    path('validate_login.html', views.validate_login),
    path('validate_signup.html', views.validate_signup),
    path('profile.html', views.profile),
    path('signout.html', views.signout),
    path('error.html', views.error),

]