from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import get_language 
#this app


class Category(models.Model):
	category_name_en = models.CharField(max_length=255)
	category_name_ht = models.CharField(max_length=255)

	def __str__(self):
		return f"{self.category_name_en} / {self.category_name_ht}"

class Tag(models.Model):
	tag_name_en = models.CharField(max_length=255)
	tag_name_ht = models.CharField(max_length=255)

	def __str__(self):
		return f"{self.tag_name_en} / {self.tag_name_ht}"

class Comment(models.Model):
	content = models.TextField()
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	like_counter = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Comment by {self.created_by.username}"

class Article(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag)
	article_title_en = models.CharField(max_length=255)
	article_title_ht = models.CharField(max_length=255)
	article_content_en = models.TextField()
	article_content_ht = models.TextField()
	contributors = models.ManyToManyField(User, related_name="article_contributors")
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article_creator")
	created_at = models.DateTimeField(auto_now_add=True)
	time_to_read = models.PositiveIntegerField()
	like_counter = models.PositiveIntegerField(default=0)

	def __str__(self):
		return f"{self.article_title_en} / {self.article_title_ht}" 

	def get_title(self):
		"""Get the articles title depending on current language selected"""
		current_language = get_language() 
		if current_language == 'ht':
			return self.article_title_ht
		else:
			return self.article_title_en
	def get_content(self, current_language):
		"""Get the articles content depending on current language selected"""
		current_language = get_language() 
		if current_language == 'ht':
			return self.article_title_ht
		else:
			return self.article_title_en

	



