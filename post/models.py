from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
	img_url = models.URLField(max_length=200)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	name = models.CharField(max_length=30, default='')
	#comments = models.


	def __str__(self):
		return self.name


class Like(models.Model):
	count = models.IntegerField()
	post = models.OneToOneField(Post, on_delete=models.CASCADE)

	def __str__(self):
		return 'likes for ' + self.post.name


class Comment(models.Model):
	text = models.TextField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	parent = models.ForeignKey(Post, on_delete=models.CASCADE)

	def __str__(self):
		return 'comment for ' + self.parent.name + ' from ' + self.owner.username

