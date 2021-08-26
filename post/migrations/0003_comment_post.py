# Generated by Django 3.2.4 on 2021-08-26 20:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_customuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', related_query_name='comment', to='post.post'),
            preserve_default=False,
        ),
    ]
