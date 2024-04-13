from django import template
from ..models import Article 

register = template.Library()

@register.filter(name='get_article_title')
def get_article_title(article, current_language):
	return article.get_title(current_language)

@register.filter(name='get_article_content')
def get_article_content(article, current_language):
	return article.get_content(current_language)
	


