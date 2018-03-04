from django.urls import path
from django.contrib import admin
from articles import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.article_list, name='article-list'),
    path('create/', views.article_create, name='article-create'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('update/<int:article_id>/', views.article_update, name='article-update'),
    path('delete/<int:article_id>/', views.article_delete, name='article-delete'),

    path('like/<int:article_id>/', views.like, name='like-button'),    

]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)