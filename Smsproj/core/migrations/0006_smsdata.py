# Generated by Django 3.1.7 on 2021-07-09 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_totp'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txt', models.CharField(max_length=500)),
            ],
        ),
    ]
