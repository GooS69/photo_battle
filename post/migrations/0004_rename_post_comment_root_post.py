# Generated by Django 3.2.4 on 2021-08-26 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_comment_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='root_post',
        ),
    ]