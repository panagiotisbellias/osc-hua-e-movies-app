from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('movies/', views.index, name='index'),
    path('movies/<int:movie_id>/', views.detail, name='detail'),
    path('movies/<int:movie_id>/rate/', views.rate, name='rate'),

    path('movies/create/', views.create, name='create'),
    path('movies/new_movie', views.new_movie, name='new_movie'),
    path('movies/<int:movie_id>/delete/', views.delete, name='delete'),
    path('movies/suggestions/', views.suggested, name='create_from_api'),
    
    path('about/', views.about, name='about'),
]