from django.shortcuts import render
from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	CreateAPIView,
	DestroyAPIView,
	RetrieveUpdateAPIView
	)
from articles.models import Article, Like
from .serializers import (
	ArticleListSerializer,
	ArticleDetailSerializer,
	ArticleCreateSerializer,
	LikeCreateSerializer,
	RegisterUserSerializer,
	UserLoginSerializer
	)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsAuthorOrStaff
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import requests
from django.urls import reverse
from django.http import JsonResponse
import json

def test_list_view(request):
	url = 'http://127.0.0.1:8000/api/list/'
	response = requests.get(url)
	# stuff = json.loads(response)
	return JsonResponse(response.json(), safe=False)



class LoginAPIView(APIView):
	permission_classes = [AllowAny]
	serializer_class = UserLoginSerializer

	def post(self, request, format=None):
		my_data = request.data
		my_serializer = UserLoginSerializer(data=my_data)
		if my_serializer.is_valid(raise_exception=True):
			new_data = my_serializer.data
			return Response(new_data, status=HTTP_200_OK)
		return Response(my_serializer.errors, status=HTTP_400_BAD_REQUEST)



class UserRegisterView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegisterUserSerializer
	permission_classes = [AllowAny]


class ArticleListView(ListAPIView):
	queryset = Article.objects.all()
	serializer_class = ArticleListSerializer
	permission_classes = [AllowAny,]
	filter_backends = [SearchFilter,OrderingFilter]
	search_fields = ['title', 'content', 'author__username']

class ArticleDetailView(RetrieveAPIView):
	queryset = Article.objects.all()
	serializer_class = ArticleDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'article_id'
	permission_classes = [AllowAny,]

class ArticleCreateView(CreateAPIView):
	queryset = Article.objects.all()
	serializer_class = ArticleCreateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

class ArticleDeleteView(DestroyAPIView):
	queryset = Article.objects.all()
	serializer_class = ArticleDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'article_id'
	permission_classes = [IsAuthenticated,IsAuthorOrStaff]	

class ArticleUpdateView(RetrieveUpdateAPIView):
	queryset = Article.objects.all()
	serializer_class = ArticleDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'article_id'
	permission_classes = [IsAuthenticated,IsAuthorOrStaff]

class LikeCreateView(CreateAPIView):
	queryset = Like.objects.all()
	serializer_class = LikeCreateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)

