import re

from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver


class Post(models.Model):
	POST_SAVE_FIELDS = ['img_large']

	@staticmethod
	def image_path(self, filename):
		path = re.sub(r'(\d.+)(\d{3})(\d{3})$', r'\1/\2/\3', '{0:09d}'.format(self.id))
		return f"{self.__class__.__name__.lower()}s/{path}/img_large/{filename}"

	img_large = models.ImageField(upload_to=image_path.__func__)
	name = models.CharField(max_length=255)
	pub_date = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey('auth.user', on_delete=models.CASCADE, related_name='posts', related_query_name='post')
	number_of_likes = models.IntegerField(default=0)
	number_of_comments = models.IntegerField(default=0)

	POST_STATUS = (
		('v', 'Verified'),
		('n', 'Not verified'),
		('r', 'Rejected'),
	)

	status = models.CharField(max_length=1, choices=POST_STATUS, default='n')

	def __str__(self):
		return self.name

	class Meta:
		db_table = "posts"
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'
		ordering = ['-number_of_likes']


@receiver(pre_save, sender=Post)
def skip_saving_file(sender, instance, **kwargs):
	if not instance.id:
		for field in instance.POST_SAVE_FIELDS:
			if not hasattr(instance, f"post_save_{field}_field"):
				setattr(instance, f"post_save_{field}_field", getattr(instance, field))
			setattr(instance, field, None)


@receiver(post_save, sender=Post)
def save_file(sender, instance, created, **kwargs):
	if created:
		for field in instance.POST_SAVE_FIELDS:
			if hasattr(instance, f"post_save_{field}_field"):
				setattr(instance, field, getattr(instance, f"post_save_{field}_field"))
		instance.save()


@receiver(post_delete, sender=Post)
def delete_file(sender, instance, *args, **kwargs):
	instance.img_large.storage.delete(instance.img_large.name)
