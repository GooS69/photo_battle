# Generated by Django 3.2.4 on 2021-06-09 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_like_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='count',
        ),
    ]