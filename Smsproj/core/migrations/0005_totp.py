# Generated by Django 3.1.7 on 2021-07-06 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210705_1358'),
    ]

    operations = [
        migrations.CreateModel(
            name='TOTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=6)),
            ],
        ),
    ]
