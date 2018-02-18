from django.db import models

class Article(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	author = models.CharField(max_length=100)

	def __str__(self):
		return self.title