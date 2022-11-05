# Generated by Django 3.2.5 on 2022-11-05 04:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0017_todoitem_todo_list'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['date_added', 'last_updated']},
        ),
        migrations.AlterModelOptions(
            name='resource',
            options={'ordering': ['date_added', 'last_updated']},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['date_added', 'last_updated']},
        ),
        migrations.AlterModelOptions(
            name='timetable',
            options={'ordering': ['date_added', 'last_updated']},
        ),
        migrations.AlterModelOptions(
            name='timetableactivity',
            options={'ordering': ['date_added', 'last_updated']},
        ),
        migrations.AlterModelOptions(
            name='todo',
            options={'ordering': ['date_added', 'last_updated']},
        ),
        migrations.AlterModelOptions(
            name='todoitem',
            options={'ordering': ['date_added', 'last_updated']},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['date_added', 'last_updated']},
        ),
        migrations.AddField(
            model_name='course',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resource',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='section',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='timetable',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='timetable',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='timetableactivity',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='timetableactivity',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='todo',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='todo',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='todoitem',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='todoitem',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
