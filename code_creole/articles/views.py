#django
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import get_language 
from django.utils.translation import activate
#Django
from django.utils.translation import gettext as _
from django.contrib.auth import login , logout, authenticate, get_user_model, update_session_auth_hash
from django.contrib import messages
from .models import Article, Category, Tag 
from .handlers import format_content

#this app
from .forms import LoginForm

#python 
import json

#third partys 
import requests 
# Create your views here.

AVAILABLE_LANGUAGES = ['en', 'ht']
LANGUAGE_SESSION_KEY = 'django_language'


def sign_up(request):
	return render(request, 'articles/sign-up.html')

def login_view(request):
	if request.method == "GET":
		form = LoginForm()
		context = {"form":form}
		return render(request, "articles/login.html", context)


	if request.method == "POST":
		form = LoginForm(request.POST or None)
		if form.is_valid(): #Captcha is checked on form validation
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				try:
					login(request, user)
					
					return redirect('home')
				except Exception as e:
					messages.error(request, f"{e}")
					return redirect("login_view")
			else:
				messages.error(request, "Invalid username/password.")
				return redirect("login_view")
		else: 
			messages.error(request, "Invalid username/password.")
			return redirect("login_view")


def logout_view(request):
	logout(request)
	return redirect('home')

def home(request):
	if request.method == "GET":
		articles = Article.objects.all().order_by("-created_at")
		categories = Category.objects.all() 
		tags = Tag.objects.all() 
		#search_form_here
		
		return render(request, 'articles/home.html', {'articles': articles})

def article_detail_view(request, article_id):
	current_language = get_language()
	article = get_object_or_404(Article, pk=article_id)
	raw_article_content = article.get_content()
	formatted_content = format_content(raw_article_content)
	context = {"article":article, "formatted_content":formatted_content, "current_language":current_language} 
	return render(request, 'articles/article_detail.html', context)

@csrf_exempt
def set_language(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		language = data.get('language')
		if language in AVAILABLE_LANGUAGES:
			activate(language)
			request.session[LANGUAGE_SESSION_KEY] = language
			return JsonResponse({'status': 'success', 'language': language})
		else:
			return JsonResponse({'status': 'error', 'message': 'Invalid language selected'}, status=400)
	return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


