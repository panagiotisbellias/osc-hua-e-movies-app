from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='home'),
    path('movies/', views.index, name='index'),
    path('movies/<int:movie_id>/', views.detail, name='detail'),
]