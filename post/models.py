from django.db import models


class User(models.Model):
	name = models.CharField(max_length=30, default='')

	def __str__(self):
		return self.name


class Post(models.Model):
	img_url = models.URLField(max_length=200)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=30, default='')

	def __str__(self):
		return self.name
