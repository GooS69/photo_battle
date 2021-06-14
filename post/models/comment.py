from django.db import models


class Comment(models.Model):
	text = models.TextField()
	author = models.ForeignKey('auth.user', on_delete=models.CASCADE)
	post = models.ForeignKey('post', on_delete=models.CASCADE)
	parent = models.ForeignKey('self', on_delete=models.CASCADE,null=True)

	def __str__(self):
		return 'comment for ' + self.post.name + ' from ' + self.author.username

