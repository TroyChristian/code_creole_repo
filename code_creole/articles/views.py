#django
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import get_language 
from django.utils.translation import gettext_lazy as _
from django.utils.translation import activate
#Django
from django.utils.translation import gettext as _
from django.contrib.auth import login , logout, authenticate, get_user_model, update_session_auth_hash
from django.contrib import messages
from .models import Article, Category, Tag 
import articles.handlers as h


#this app
from .forms import LoginForm, RegistrationForm

#python 
import json

#third partys 
import requests 
# Create your views here.

AVAILABLE_LANGUAGES = ['en', 'ht']
LANGUAGE_SESSION_KEY = 'django_language'


def sign_up(request):
	if request.method == "GET":
		if request.session.get('is_currently_logged_in'):
			return redirect("home")
		form = RegistrationForm()
		context = {'form':form}
		return render(request, 'articles/sign-up.html', context)
	if request.method == "POST":
		form = RegistrationForm(request.POST or None)
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password'] 
			user.set_password(password)
			user.save() #create the user
			user = authenticate(username=username, password=password) #log the user in so we can send them to the home page.
			login(request, user)
			request.session['is_currently_logged_in'] = True #set is currently logged in 
			messages.success(request, _("Account created!  Welcome to Code Creole!"))
			return redirect("login_view") 
		else:
			messages.error(request, _("An error occured during your request. Please try again."))
			return redirect("sign_up")


def login_view(request):
	if request.method == "GET":
		if request.session.get('is_currently_logged_in'):
			return redirect("home")
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
					request.session['is_currently_logged_in'] = True #set is currently logged in 
					return redirect('home')
				except Exception as e:
					messages.error(request, f"{e}")
					return redirect("login_view")
			else:
				messages.error(request, _("Invalid username/password."))
				return redirect("login_view")
		else: 
			messages.error(request, _("Invalid username/password."))
			return redirect("login_view")


def logout_view(request):
	try:
		del request.session['is_currently_logged_in']
	except KeyError:
		pass
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
	formatted_content = h.format_content(raw_article_content)
	user_likes_article = h.check_if_article_liked(request.user, article)
	context = {"article":article, "formatted_content":formatted_content, "current_language":current_language, "user_likes_article":user_likes_article} 
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


@require_POST
def like_article(request, article_id):

	user = request.user
	article = get_object_or_404(Article, pk=article_id)

	if not "is_currently_logged_in" in request.session:
		messages.error(request, _("You must be logged in to like an article."))
		return redirect("article_detail", article.pk)

	if h.like_article(user, article):
		messages.success(request, _("You liked this article."))
		return redirect("article_detail", article.pk)
	else:
		return redirect("article_detail", article.pk)

@require_POST
def unlike_article(request, article_id):
	user = request.user 
	article = get_object_or_404(Article, pk=article_id)
	if not "is_currently_logged_in" in request.session:
		messages.error(request, _("You must be logged in to unlike an article."))
		return redirect("article_detail", article.pk)

	if h.unlike_article(user, article):
		messages.success(request, _("You unliked this article."))
		return redirect("article_detail", article.pk)
	else:
		return redirect("article_detail", article.pk)
