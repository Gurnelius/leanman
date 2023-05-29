from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('update/', views.save_data_from_csv, name="update"),
    path('popular/', views.popular, name="popular"),
    path('masculinity/', views.masculinity_saturday, name="masculinity"),
    path('stats/', views.stats, name="stats"),
    path('search/', views.search, name="search"),
    path('wordcloud/', views.word_cloud, name="wordcloud"),
    path('hashtags/<str:hashtag>', views.hashtag, name='hashtags'),
    path('hashtags/', views.hashtag, name='hashtags'),


]

