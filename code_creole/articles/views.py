#django
from django.shortcuts import render
from django.views.generic import ListView
from .models import Article
from django.utils.translation import get_language

#third partys 
import requests
# Create your views here.

def home(request):
	current_language = get_language()
	#response = requests.get('http://localhost:8000/api/')
	articles = Article.objects.all()
	return render(request, 'articles/article_list.html', {'article_list': articles, 'current_language': current_language})

