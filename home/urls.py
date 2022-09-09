# from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.home, name="home"),
    path('help', views.help, name="help"),
    path('logout', views.logoutUser, name="logout"),
    path('change_password', views.change_password, name="change_password"),
    path('add_material/<str:inv_id>', views.add_material, name='add_material'),
    path('inventory/<str:inv_id>', views.inventory, name='inventory')
]
