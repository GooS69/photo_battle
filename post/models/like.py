from django.db import models


class Like(models.Model):
    users = models.ManyToManyField('auth.user',related_name='users')
    post = models.OneToOneField('post', on_delete=models.CASCADE)