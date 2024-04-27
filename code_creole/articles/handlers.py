from django.utils.translation import get_language 
from .models import *
def format_content(content):
    # Simple Python function to replace markdown code blocks with HTML
    content = content.replace("<code-block>", "<pre class='code-block'><code>")
    content = content.replace("</code-block>", "</code></pre>")
    content = content.replace("<inline-code>", "<span class='inline-code'>")
    content = content.replace("</inline-code>", "</span>")
    return content 

def like_article(user, article):
	user_liked_articles_qs = UserLikesArticle.objects.filter(user=user.pk, article=article)
	if len(user_liked_articles_qs) > 0:
		print("This user has already liked this article")
		return False
	UserLikesArticle.objects.create(article=article, user=user)
	article.like_count += 1
	article.save()
	print("Liked Article!")
	return True 

def unlike_article(user, article):
	user_liked_articles_qs = UserLikesArticle.objects.filter(user=user.pk, article=article)
	if len(user_liked_articles_qs) > 0:
		article_like = user_liked_articles_qs.first()
		article_like.delete() 
		article.like_count -= 1
		article.save() 
		print("Unliked!")
		return True
	else:
		print("Article not liked by user - so it cannot be unliked")
		return False

def check_if_article_liked(user, article):
		if UserLikesArticle.objects.filter(user=user.pk, article=article).exists():
			return True 
		return False 



### Threads and ThreadMessages ###
# Helper Function 1: Add participants to the thread
def add_participants_to_thread(thread, participants):
	thread.participants.add(*participants)


# Helper Function 2: Add a message to the thread
def add_thread_message_to_thread(thread, sender, body):
	message = ThreadMessage(thread=thread, sender=sender, body=body)
	message.save()
	


def get_thread_messages_in_thread(thread):
	thread_messages = ThreadMessage.objects.filter(thread=thread)
	return thread_messages



def remove_participants_from_thread(thread, participants):
	thread.participants.remove(*participants) 


