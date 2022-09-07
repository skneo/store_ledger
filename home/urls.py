# from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.home, name="home"),
    path('logout', views.logoutUser, name="logout"),
    path('change_password', views.change_password, name="change_password")
]
