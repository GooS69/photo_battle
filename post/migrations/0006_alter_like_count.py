# Generated by Django 3.2.4 on 2021-06-09 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]