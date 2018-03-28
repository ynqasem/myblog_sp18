from django.contrib import admin
from .models import Article, Like

admin.site.register(Article)

admin.site.register(Like)