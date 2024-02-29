from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleAPIView

#router = DefaultRouter()
#router.register(r'articles', ArticleViewSet)

urlpatterns = [
	path('', ArticleAPIView.as_view()),
	#path('', include(router.urls)),
]
