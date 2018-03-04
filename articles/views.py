from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Article, Like
from .forms import ArticleForm, UserRegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout

def like(request, article_id):
	article_obj = Article.objects.get(id=article_id)

	like_obj, created = Like.objects.get_or_create(user=request.user, article=article_obj)

	if created:
		action="like"
	else:
		action="unlike"
		like_obj.delete()

	like_count = article_obj.like_set.all().count()
	# like_count = Like.objects.filter(article=article_obj)

	context = {
		"action":action,
		"count":like_count
	}
	return JsonResponse(context, safe=False)

def user_register(request):
	form = UserRegisterForm()
	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			person = form.save(commit=False)
			person.set_password(person.password)
			person.save()
			login(request, person)
			return redirect("article-list")
	context = {
		"form":form
	}
	return render(request, 'register.html', context)

def user_logout(request):
	logout(request)
	return redirect('login')

def user_login(request):
	form = LoginForm()
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			my_username = form.cleaned_data['username']
			my_password = form.cleaned_data['password']
			auth_user = authenticate(username=my_username, password=my_password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect("article-list")
	context = {
		"form":form
	}
	return render(request, 'login.html', context)

def article_list(request):
	object_list = Article.objects.all()
	object_list = object_list.order_by('created', 'title')
	query = request.GET.get('q')
	if query:
		object_list = object_list.filter(title__contains=query)

	liked_articles = []
	likes = request.user.like_set.all()
	for like in likes:
		liked_articles.append(like.article)

	context = {
		"articles": object_list,
		"my_likes": liked_articles
	}
	return render(request, 'list.html', context)

def article_create(request):
	form = ArticleForm()
	if request.method == "POST":
		form = ArticleForm(request.POST, request.FILES or None)
		if form.is_valid():
			article_obj = form.save(commit=False)
			article_obj.author = request.user
			article_obj.save()
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