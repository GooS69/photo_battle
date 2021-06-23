from django.db import models


class Post(models.Model):
	img_large = models.ImageField(upload_to='img')
	name = models.CharField(max_length=255)
	pub_date = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey('auth.user', on_delete=models.CASCADE, related_name='posts', related_query_name='post')
	number_of_likes = models.IntegerField(default=0)

	POST_STATUS = (
		('v', 'Verified'),
		('n', 'Not verified'),
		('r', 'Rejected'),
	)

	status = models.CharField(max_length=1, choices=POST_STATUS, default='n')

	def delete(self, using=None, keep_parents=False):
		self.img_large.storage.delete(self.img_large.name)
		super().delete()

	def __str__(self):
		return self.name

	class Meta:
		db_table = "posts"
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'
