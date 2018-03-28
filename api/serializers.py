from rest_framework import serializers
from articles.models import Article, Like
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings

class UserLoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField(style={'input_type':'password'}, write_only=True)
	token = serializers.CharField(allow_blank=True, read_only=True)

	def validate(self, data):
		my_username = data.get('username')
		my_password = data.get('password')

		if my_username == '':
			raise serializers.ValidationError("A username is required to login.")

		try:
			user_obj = User.objects.get(username=my_username)
		except:
			raise serializers.ValidationError("This username does not exist")

		if not user_obj.check_password(my_password):
			raise serializers.ValidationError("Incorrect username/password combination! Noob..")


		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

		payload = jwt_payload_handler(user_obj)
		token = jwt_encode_handler(payload)

		data["token"] = token
		return data


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name']

class ArticleListSerializer(serializers.ModelSerializer):
	detail_page = serializers.HyperlinkedIdentityField(
		view_name = 'api-detail',
		lookup_field = 'id',
		lookup_url_kwarg = 'article_id'
		)
	# author = serializers.SerializerMethodField()
	author = UserSerializer()

	class Meta:
		model = Article
		fields = ['id', 'author', 'title', 'detail_page',]

	# def get_author(self, obj):
	# 	return obj.author.username

class LikeCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Like
		fields = ['article']

class LikeListSerializer(serializers.ModelSerializer):
	user = UserSerializer()

	class Meta:
		model = Like
		fields = ['user']
	

class ArticleDetailSerializer(serializers.ModelSerializer):
	likes = serializers.SerializerMethodField()

	class Meta:
		model = Article
		fields = ['id', 'title', 'content', 'author', 'publish_date', 'likes']

	def get_likes(self, obj):
		# likes = Like.objects.filter(article=obj)
		likes = obj.like_set.all()
		json_likes = LikeListSerializer(likes, many=True).data
		return json_likes



class ArticleCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = ['title','content','image']


class RegisterUserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(style={'input_type':'password'}, write_only=True)
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password']

	def create(self, validated_data):
		new_user = User(**validated_data)
		new_user.set_password(validated_data['password'])
		new_user.save()
		return validated_data
