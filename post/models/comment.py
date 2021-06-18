from django.db import models


class Comment(models.Model):
	text = models.TextField()
	author = models.ForeignKey('auth.user', on_delete=models.CASCADE, related_name='comments', related_query_name='comment')
	post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments', related_query_name='comment')
	parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None, blank=True, related_name='comments', related_query_name='comment')

	def __str__(self):
		return 'comment for ' + self.post.name + ' from ' + self.author.username

	class Meta:
		db_table = "comments"
		verbose_name = 'Коментарий'
		verbose_name_plural = 'Коментарии'
