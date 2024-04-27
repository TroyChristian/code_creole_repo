from django.contrib import admin
from .models import Category, Tag,  Article, UserLikesArticle, Thread, ThreadMessage
# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)

admin.site.register(Article)
admin.site.register(UserLikesArticle)
admin.site.register(Thread)
admin.site.register(ThreadMessage)