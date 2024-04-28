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
from .models import Article, Category, Tag, Thread, ThreadMessage, UserSavesArticle
import articles.handlers as h


#this app
from .forms import LoginForm, RegistrationForm, CommentForm

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
	if request.method == "GET":
		current_language = get_language()
		article = get_object_or_404(Article, pk=article_id)
		raw_article_content = article.get_content()
		formatted_content = h.format_content(raw_article_content)
		user_likes_article = h.check_if_article_liked(request.user, article)
		article_saved = h.check_if_article_saved(request.user, article)
		form = CommentForm()
		num_comments = 0
		comments = []
		if article.thread:
			comments = h.get_thread_messages_in_thread(article.thread)
			num_comments = len(comments)

		context = {"article":article, "formatted_content":formatted_content, "current_language":current_language, "user_likes_article":user_likes_article, "form":form, "comments":comments, "num_comments":num_comments, "article_saved":article_saved} 
		return render(request, 'articles/article_detail.html', context)

	if request.method == "POST":
		if "comment_form" in request.POST:
			article = get_object_or_404(Article, pk=article_id)
			if article.thread and article.thread.locked:
				messages.warning(request, _("Cannot comment in a locked thread."))
				return redirect(request.path)
			
			if not article.thread:
				thread = Thread.objects.create()
				article.thread = thread 
				article.save() 
			article_thread = article.thread 
			comment_form = CommentForm(request.POST or None)
			if comment_form.is_valid():
				h.add_participants_to_thread(article_thread, [request.user]) #add the commenting user to the thread
				sender = request.user
				body = comment_form.cleaned_data.get("body")
				h.add_thread_message_to_thread(article_thread, sender, body) #creates ThreadMessage, marks it read for the sender.
				messages.success(request, _("Comment Created"))
				return redirect(request.path)
			else:
				messages.error(request, _("Failed to add comment."))
				return redirect(request.path)


def saved_articles(request):
	if "is_currently_logged_in" not in request.session:
		messages.error(request, _("You must log in to view your saved articles."))
		return redirect("login_view")
	user_saves_article_qs = UserSavesArticle.objects.filter(user=request.user)
	saved_articles = []
	for user_saves_article_instance in user_saves_article_qs:
		saved_articles.append(user_saves_article_instance.article)

	context = {"saved_articles":saved_articles}
	return render(request, 'articles/saved_articles.html', context)

@require_POST
def save_article(request, article_pk):
	
	if request.method == "POST":
		user = request.user
		article = get_object_or_404(Article, pk=article_pk)

		try:
			UserSavesArticle.objects.create(article=article, user=user)
			messages.success(request, _("Article saved!"))
			return redirect("article_detail", article.pk) 
		except Exception as e:
			messages.error(request, _("Error occured saving article."))
			return redirect("article_detail", article.pk) 

@require_POST
def unsave_article(request, article_pk):
	if request.method == "POST":
		user = request.user
		article = get_object_or_404(Article, pk=article_pk)

		try:
			user_saves_article_instance = UserSavesArticle.objects.get(article=article, user=user)
			user_saves_article_instance.delete()
			messages.success(request, _("Action Successful."))
			return redirect("article_detail", article.pk) 
		except Exception as e:
			messages.error(request, _("Action Failed"))
			return redirect("article_detail", article.pk) 

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

@require_POST
def delete_comment(request, article_id, thread_message_id ):
	comment = get_object_or_404(ThreadMessage, pk=thread_message_id)
	if comment.sender == request.user: #ensure the user can only delete their own comments
		comment.delete()
		messages.success(request, _("Comment Deleted"))
		return redirect("article_detail", article_id)
	else:
		return redirect("article_detail", article_id)



@require_POST
def save_comment(request):
    import json
    data = json.loads(request.body)
    comment_id = data['commentId']
    new_text = data['text']

    try:
        comment = ThreadMessage.objects.get(pk=comment_id)
        comment.body = new_text
        comment.save()
        return JsonResponse({'status': 'success'})
    except Comment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Comment not found'}, status=404)