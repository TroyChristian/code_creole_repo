from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import get_language 
from django.urls import reverse
#this app

#third parties
#PIL
#from PIL import Image
from PIL import Image as PILImage
from pilkit.processors import ResizeToFill
from pilkit.processors import ResizeToFit


#Django Image Kit 
from imagekit.models import ProcessedImageField
from imagekit.models import ImageSpecField
from imagekit.processors import Adjust

class Thread(models.Model):
	participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='threads')
	locked = models.BooleanField(default=False)
	def __str__(self):
		return f'Thread #{self.pk}'

	def get_num_messages_in_thread(self):
		thread_messages = ThreadMessage.objects.filter(thread=self.pk)
		if thread_messages:
			return len(thread_messages)
		else:
			return 0


class ThreadMessage(models.Model):
	thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	body = models.TextField()
	edited = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['created_at'] 


	def __str__(self):
		return f'Message #{self.pk}'

class Category(models.Model):
	category_name_en = models.CharField(max_length=255)
	category_name_ht = models.CharField(max_length=255)
	def get_category_name(self):
		"""Get the articles title depending on current language selected"""
		current_language = get_language() 
		if current_language == 'ht':
			return self.category_name_ht
		else:
			return self.category_name_en

	def __str__(self):
		return f"{self.category_name_en} / {self.category_name_ht}"

class Tag(models.Model):
	tag_name_en = models.CharField(max_length=255)
	tag_name_ht = models.CharField(max_length=255)

	def __str__(self):
		return f"{self.tag_name_en} / {self.tag_name_ht}"



class Article(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	thread = models.ForeignKey(Thread, on_delete=models.SET_NULL, null=True, blank=True)
	tags = models.ManyToManyField(Tag)
	article_title_en = models.CharField(max_length=255)
	article_title_ht = models.CharField(max_length=255)
	article_content_en = models.TextField()
	article_content_ht = models.TextField()
	main_image = models.ImageField(upload_to="article_main_images", null=True, blank=True) #if is main image show in LTD and in gallery view, else show static/defaults/no_image_available
	thumbnail = ImageSpecField(source="main_image", processors=[ResizeToFit(433,243)], format="JPEG", options={"qaulity":100}) #show on listing card if is main image
	contributors = models.ManyToManyField(User, related_name="article_contributors")
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article_creator")
	created_at = models.DateTimeField(auto_now_add=True)
	time_to_read = models.PositiveIntegerField()
	like_count = models.PositiveIntegerField(default=0)

	def __str__(self):
		return f"{self.article_title_en} / {self.article_title_ht}" 

	def get_title(self):
		"""Get the articles title depending on current language selected"""
		current_language = get_language() 
		if current_language == 'ht':
			return self.article_title_ht
		else:
			return self.article_title_en
	def get_content(self):
		"""Get the articles content depending on current language selected"""
		current_language = get_language() 
		if current_language == 'ht':
			return self.article_content_ht
		else:
			return self.article_content_en 

	def get_contributors(self):
		return list(self.contributors.all())

	def get_absolute_url(self):
		# Assuming you have a URL pattern named 'article_detail' that takes an 'article_id'
		return reverse('article_detail', args=[str(self.id)])


class UserLikesArticle(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	article = models.ForeignKey(Article, on_delete=models.CASCADE)
	

	class Meta:
		unique_together = ("user", "article")

