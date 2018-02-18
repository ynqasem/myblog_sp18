from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm

def article_list(request):
	object_list = Article.objects.all()
	context = {
		"articles": object_list
	}
	return render(request, 'list.html', context)

def article_create(request):
	form = ArticleForm()
	if request.method == "POST":
		form = ArticleForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("article-list")
	context = {
		"form":form
	}
	return render(request, 'create.html', context)

def article_update(request, article_id):
	article = Article.objects.get(id=article_id)
	form = ArticleForm(instance=article)
	if request.method == "POST":
		form = ArticleForm(request.POST, instance=article)
		if form.is_valid():
			form.save()
			return redirect("article-list")
	context = {
		"article":article,
		"form":form
	}
	return render(request, 'update.html', context)

def article_delete(request, article_id):
	Article.objects.get(id=article_id).delete()
	return redirect("article-list")