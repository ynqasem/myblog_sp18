from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	image = models.ImageField(null=True)
	created = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	publish_date = models.DateField()

	def __str__(self):
		return self.title


class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	article = models.ForeignKey(Article, on_delete=models.CASCADE)