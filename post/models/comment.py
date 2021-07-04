from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation


class Comment(models.Model):
	text = models.TextField()
	author = models.ForeignKey('auth.user', on_delete=models.CASCADE, related_name='comments', related_query_name='comment')

	#post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments', related_query_name='comment')
	#parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None, blank=True, related_name='comments', related_query_name='comment')

	comments = GenericRelation('self')

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()

	def __str__(self):
		return self.text + ' from ' + self.author.username

	class Meta:
		db_table = "comments"
		verbose_name = 'Коментарий'
		verbose_name_plural = 'Коментарии'


#@receiver(pre_save, sender=Comment)
#def set_new_record_flag(sender, instance, *args, **kwargs):
#	instance.__new_record = not bool(instance.id)


#@receiver(post_save, sender=Comment)
#def incr_number_of_comments_on_post(sender, instance, *args, **kwargs):
#	if instance.__new_record:
#		instance.post.number_of_comments += 1
#		instance.post.save()


#@receiver(post_delete, sender=Comment)
#def decr_number_of_comments_on_post(sender, instance, *args, **kwargs):
#	instance.post.number_of_comments -= 1
#	instance.post.save()
