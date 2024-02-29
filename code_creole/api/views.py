from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets
from articles.models import Article
from .serializers import ArticleSerializer

class ArticleAPIView(generics.ListAPIView):
	queryset = Article.objects.all()
	serializer_class = ArticleSerializer
