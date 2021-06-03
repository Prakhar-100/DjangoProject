# Generated by Django 3.1.7 on 2021-06-01 08:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0003_auto_20210531_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatgrouplist',
            name='member_name',
        ),
        migrations.AddField(
            model_name='chatgrouplist',
            name='member_name',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]