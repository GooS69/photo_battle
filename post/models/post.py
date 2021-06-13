from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
	img_url = models.URLField(max_length=200)
	owner = models.ForeignKey('auth.user', on_delete=models.CASCADE, related_name='owner')
	likes = models.ManyToManyField('auth.user', related_name='likes')
	name = models.CharField(max_length=30, default='')

	def get_likes_count(self):
		return self.likes.count()

	def __str__(self):
		return self.name