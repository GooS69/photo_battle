from django.db import models


class Like(models.Model):
    user = models.ForeignKey('auth.user', related_name='likes', related_query_name='like', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='likes', related_query_name='like', on_delete=models.CASCADE)

    def __str__(self):
        return "like from " + self.user.first_name + " to " + self.post.name

    class Meta:
        db_table = "likes"
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        constraints = [models.UniqueConstraint(fields=['user', 'post'], name='unique_like'), ]
