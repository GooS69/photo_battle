from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
