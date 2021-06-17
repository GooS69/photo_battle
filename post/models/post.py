from django.db import models


class Post(models.Model):
	img_large = models.ImageField(upload_to='img')
	name = models.CharField(max_length=30, default='')
	pub_date = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey('auth.user', on_delete=models.CASCADE, related_name='owner')

	class Meta:
		db_table = "Post"

	def __str__(self):
		return self.name
