from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser):
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'