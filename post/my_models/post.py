import os
import re

from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from PIL import Image
from django.core.files.storage import default_storage
from django.contrib.contenttypes.fields import GenericRelation


class Post(models.Model):
	POST_SAVE_FIELDS = ['img']
	VERSION_DESCRIPTIONS = {
		'large': {
			'width': 200,
			'height': 100
		},
		'small': {
			'width': 200,
			'height': 100
		}
	}

	@staticmethod
	def image_path(self, filename):
		path = re.sub(r'(\d.+)(\d{3})(\d{3})$', r'\1/\2/\3', '{0:09d}'.format(self.id))
		return f"{self.__class__.__name__.lower()}s/{path}/img/{filename}"

	# versions=['large', 'small']
	img = models.ImageField(upload_to=image_path.__func__)
	name = models.CharField(max_length=255)
	pub_date = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='posts', related_query_name='post')
	comments = GenericRelation('Comment', related_query_name='post')
	number_of_likes = models.IntegerField(default=0)
	number_of_comments = models.IntegerField(default=0)

	POST_STATUS = (
		('verified', 'Verified'),
		('not_verified', 'Not verified'),
		('rejected', 'Rejected'),
	)

	status = models.CharField(max_length=255, choices=POST_STATUS, default='not_verified')

	def make_thumbnails(self):
		size_large = (800, 600)
		size_small = (250, 200)
		with Image.open(self.img.path) as img:
			file, ext = os.path.splitext(self.img.path)
			thumbnail_large = img.resize(size_large)
			thumbnail_large.save(file + '_large' + ext)
			thumbnail_small = img.resize(size_small)
			thumbnail_small.save(file + '_small' + ext)

	def get_img_large_url(self):
		file, ext = os.path.splitext(self.img.url)
		return f'{file}_large{ext}'

	def get_img_small_url(self):
		file, ext = os.path.splitext(self.img.url)
		return f'{file}_small{ext}'

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
	default_storage.delete(file + '_large' + ext)
	default_storage.delete(file + '_small' + ext)
