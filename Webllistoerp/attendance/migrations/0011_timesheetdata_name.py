# Generated by Django 3.1.7 on 2021-06-07 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0010_auto_20210606_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheetdata',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]