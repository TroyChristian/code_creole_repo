from django.urls import path, include
from . import views

urlpatterns = [
#articles app core
    path('', views.home, name='home'), 
    path('article/<int:article_id>', views.article_detail_view, name='article_detail'),
    path('set-language/', views.set_language, name='set-language'), 
    path('article/like/<int:article_id>', views.like_article, name='like_article'),
    path('article/unlike/<int:article_id>', views.unlike_article, name='unlike_article'),

    #registration
    path('sign_up', views.sign_up, name='sign_up'),

    #sign in & logout 
    path('login', views.login_view, name='login_view'),
    path('logout', views.logout_view, name='logout_view'),
]