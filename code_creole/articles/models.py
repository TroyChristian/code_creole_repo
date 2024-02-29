from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	category_name = models.CharField(max_length=255)

	def __str__(self):
		return self.category_name

class Tag(models.Model):
	tag_name = models.CharField(max_length=255)

	def __str__(self):
		return self.tag_name

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
	article_title_english = models.CharField(max_length=255)
	article_title_creole = models.CharField(max_length=255)
	article_content_english = models.TextField()
	article_content_creole = models.TextField()
	contributors = models.ManyToManyField(User, related_name="article_contributors")
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article_creator")
	created_at = models.DateTimeField(auto_now_add=True)
	time_to_read = models.PositiveIntegerField()
	like_counter = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.article_title_english
