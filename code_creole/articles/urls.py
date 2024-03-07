from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('article', views.article_detail_view, name='article_detail'),
]