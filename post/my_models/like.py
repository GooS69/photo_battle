from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver


class Like(models.Model):
    user = models.ForeignKey('CustomUser', related_name='likes', related_query_name='like', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='likes', related_query_name='like', on_delete=models.CASCADE)

    def __str__(self):
        return "like from " + self.user.first_name + " to " + self.post.name

    class Meta:
        db_table = "likes"
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        constraints = [models.UniqueConstraint(fields=['user', 'post'], name='unique_like'), ]


@receiver(post_save, sender=Like)
def incr_number_of_likes_on_post(sender, instance, created, *args, **kwargs):
    if created:
        instance.post.number_of_likes += 1
        instance.post.save()


@receiver(post_delete, sender=Like)
def decr_number_of_likes_on_post(sender, instance, *args, **kwargs):
    instance.post.number_of_likes -= 1
    instance.post.save()
