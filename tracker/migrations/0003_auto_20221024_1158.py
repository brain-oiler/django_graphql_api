# Generated by Django 3.2.5 on 2022-10-24 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20221024_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='public',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='timetable',
            name='public',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='todo',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]