from django.db import models


class Like(models.Model):
    user = models.ForeignKey('auth.user', related_name='likes', related_query_name='like', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='likes', related_query_name='like', on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
        self.post.number_of_likes += 1
        self.post.save()

    def __str__(self):
        return "like from " + self.user.first_name + " to " + self.post.name

    class Meta:
        db_table = "likes"
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        constraints = [models.UniqueConstraint(fields=['user', 'post'], name='unique_like'), ]
