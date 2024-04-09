#django
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Article, Category, Tag
from django.utils.translation import get_language

#third partys 
import requests
# Create your views here.

def home(request):
	current_language = get_language()
	articles = Article.objects.all().order_by("-created_at")
	categories = Category.objects.all() 
	tags = Tag.objects.all() 
	#search_form_here
	return render(request, 'articles/home.html', {'article_list': articles, 'current_language': current_language})

def article_detail_view(request):
	#article = Article.objects.get_object_or_404(pk=article_pk)
	return render(request, 'articles/article_detail.html')




