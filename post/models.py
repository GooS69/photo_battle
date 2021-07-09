
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class CustomUser(AbstractUser):
    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


from .my_models.comment import Comment
from .my_models.post import Post
from .my_models.like import Like



