# Generated by Django 3.1.7 on 2021-05-12 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_remove_userdayoffdata_leave_request_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdayoffdata',
            name='leave_request_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]