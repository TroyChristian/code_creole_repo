from django.urls import path, include
from . import views

urlpatterns = [
#articles app core
### ARTICLE PATHS ###

	path('', views.home, name='home'), 
	path('article/<int:article_id>', views.article_detail_view, name='article_detail'),
	path('saved', views.saved_articles, name='saved_articles'),
	#like/unlike articles
	path('article/like/<int:article_id>', views.like_article, name='like_article'),
	path('article/unlike/<int:article_id>', views.unlike_article, name='unlike_article'),
	path('article/delete-comment/<int:article_id>/<int:thread_message_id>', views.delete_comment, name="delete_comment"),
	#save/unsave articles 
	path('article/save/<int:article_pk>', views.save_article, name='save_article'),
	path('article/unsave/<int:article_pk>', views.unsave_article, name='unsave_article'), 
	#article search
	path('search/', views.search_articles, name='search_articles'),

### CATEGORIES PATHS ###
	path('categories', views.categories, name="categories"),




### AUTH PATHS ###
	#registration
	path('sign_up', views.sign_up, name='sign_up'),

	#sign in & logout 
	path('login', views.login_view, name='login_view'),
	path('logout', views.logout_view, name='logout_view'),


### AJAX ###
	 path('save-comment/', views.save_comment, name='save_comment'),
]