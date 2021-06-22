# Generated by Django 3.2.4 on 2021-06-22 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('v', 'Verified'), ('n', 'Not verified'), ('r', 'Rejected')], default='n', max_length=1),
        ),
    ]
