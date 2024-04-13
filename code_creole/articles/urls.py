from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('article/<int:article_id>', views.article_detail_view, name='article_detail'),
    path('set-language/', views.set_language, name='set-language'),
]