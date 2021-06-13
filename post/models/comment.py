from django.db import models


class Comment(models.Model):
	text = models.TextField()
	owner = models.ForeignKey('auth.user', on_delete=models.CASCADE)
	parent = models.ForeignKey('post', on_delete=models.CASCADE)

	def __str__(self):
		return 'comment for ' + self.parent.name + ' from ' + self.owner.username

