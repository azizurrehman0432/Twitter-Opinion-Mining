from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('cards', views.cards, name="cards"),
    path("",views.search,name="search"),
    path('home', views.index, name='index'),


]
