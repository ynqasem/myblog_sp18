from django.urls import path
from django.contrib import admin
from articles import views
from django.conf import settings
from django.conf.urls.static import static
from api.views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleDeleteView,
    ArticleUpdateView,
    LikeCreateView,
    UserRegisterView,
    LoginAPIView,
    test_list_view
    )

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

    path('api/list/', ArticleListView.as_view(), name='api-list'),
    path('api/detail/<int:article_id>/', ArticleDetailView.as_view(), name='api-detail'),
    path('api/create/', ArticleCreateView.as_view(), name='api-create'),
    path('api/delete/<int:article_id>/', ArticleDeleteView.as_view(), name='api-delete'),
    path('api/update/<int:article_id>/', ArticleUpdateView.as_view(), name='api-update'),

    path('api/like/', LikeCreateView.as_view(), name='api-like'),

    path('api/register/', UserRegisterView.as_view(), name='api-register'),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),

    path('test/list/', test_list_view, name='test-list'),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)