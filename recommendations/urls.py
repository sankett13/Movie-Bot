from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recommend-by-genre/', views.recommend_by_genre, name='recommend_by_genre'),
    path('recommend-by-movie/', views.recommend_by_movie, name='recommend_by_movie'),
]