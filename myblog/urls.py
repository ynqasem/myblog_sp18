from django.urls import path
from django.contrib import admin
from articles import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.article_list, name='article-list'),
    path('create/', views.article_create, name='article-create'),

    path('update/<int:article_id>/', views.article_update, name='article-update'),
    path('delete/<int:article_id>/', views.article_delete, name='article-delete'),

]
