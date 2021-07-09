import re
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    POST_SAVE_FIELDS = ['avatar']

    @staticmethod
    def image_path(self, filename):
        path = re.sub(r'(\d.+)(\d{3})(\d{3})$', r'\1/\2/\3', '{0:09d}'.format(self.id))
        return f"{self.__class__.__name__.lower()}s/{path}/avatar/{filename}"

    avatar = models.ImageField(upload_to=image_path.__func__, null=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
