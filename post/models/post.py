from django.db import models


class Post(models.Model):
	img_url = models.URLField(max_length=200)
	owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='owner')
	likes = models.ManyToManyField('User', related_name='likes')
	name = models.CharField(max_length=30, default='')

	def get_likes_count(self):
		return self.likes.count()

	def __str__(self):
		return self.name