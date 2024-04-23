#django
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import get_language 
from django.utils.translation import activate
from django.utils.translation import gettext as _
from .models import Article, Category, Tag


#python 
import json

#third partys 
import requests
# Create your views here.

AVAILABLE_LANGUAGES = ['en', 'ht']
LANGUAGE_SESSION_KEY = 'django_language'

def home(request):
	articles = Article.objects.all().order_by("-created_at")
	categories = Category.objects.all() 
	tags = Tag.objects.all() 
	#search_form_here
	
	return render(request, 'articles/home.html', {'articles': articles})

def article_detail_view(request, article_id):
	article = get_object_or_404(Article, pk=article_id)
	context = {"article":article}
	return render(request, 'articles/article_detail.html', context)

@csrf_exempt
def set_language(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		language = data.get('language')
		import pdb; pdb.set_trace()
		if language in AVAILABLE_LANGUAGES:
			activate(language)
			request.session[LANGUAGE_SESSION_KEY] = language
			return JsonResponse({'status': 'success', 'language': language})
		else:
			return JsonResponse({'status': 'error', 'message': 'Invalid language selected'}, status=400)
	return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


