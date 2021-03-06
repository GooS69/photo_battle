from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


from post.my_models.target_base_class import TargetBaseClass


class Comment(TargetBaseClass):
    root_post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='all_comments',
                                  related_query_name='comment')
    text = models.TextField()
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='comments',
                               related_query_name='comment')
    target = models.ForeignKey('TargetBaseClass', on_delete=models.CASCADE, related_name='comments',
                               related_query_name='inner_comment')

    def __str__(self):
        return self.text + ' from ' + self.author.username

    class Meta:
        db_table = "comments"
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'


@receiver(post_save, sender=Comment)
def incr_number_of_comments_on_post(sender, instance, created, *args, **kwargs):
    if created:
        root_post = instance.root_post
        root_post.number_of_comments += 1
        root_post.save()


@receiver(pre_delete, sender=Comment)
def decr_number_of_comments_on_post(sender, instance, *args, **kwargs):
    root_post = instance.root_post
    root_post.number_of_comments -= 1
    root_post.save()
