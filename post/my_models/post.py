import os
import re

from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from PIL import Image
from django.core.files.storage import default_storage

from post.my_models.target_base_class import TargetBaseClass


class Post(TargetBaseClass):
	POST_SAVE_FIELDS = ['img']
	IMAGE_SIZES = {
		'_large': (800, 600),
		'_small': (250, 200)
	}

	@staticmethod
	def image_path(self, filename):
		path = re.sub(r'(\d.+)(\d{3})(\d{3})$', r'\1/\2/\3', '{0:09d}'.format(self.id))
		return f"{self.__class__.__name__.lower()}s/{path}/img/{filename}"

	img = models.ImageField(upload_to=image_path.__func__)
	name = models.CharField(max_length=255)
	pub_date = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='posts', related_query_name='post')
	number_of_likes = models.IntegerField(default=0)
	number_of_comments = models.IntegerField(default=0)

	POST_STATUS = (
		('verified', 'Verified'),
		('not_verified', 'Not verified'),
		('rejected', 'Rejected'),
	)

	status = models.CharField(max_length=255, choices=POST_STATUS, default='not_verified')

	def make_thumbnails(self):
		with Image.open(self.img.path) as img:
			file, ext = os.path.splitext(self.img.path)
			for size in self.IMAGE_SIZES.items():
				thumbnail = img.resize(size[1])
				thumbnail.save(file + size[0] + ext)

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
		instance.make_thumbnails()


@receiver(post_delete, sender=Post)
def delete_file(sender, instance, *args, **kwargs):
	file, ext = os.path.splitext(instance.img.path)
	default_storage.delete(file + ext)
	for size in instance.IMAGE_SIZES.items():
		default_storage.delete(file + size[0] + ext)

