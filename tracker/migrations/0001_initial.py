# Generated by Django 3.2.5 on 2022-11-15 17:08

import cloudinary_storage.storage
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Course name', max_length=255)),
                ('start_date', models.DateField(blank=True, help_text='When will the user start taking this course', null=True)),
                ('end_date', models.DateField(blank=True, help_text='End date for course. Can be left null', null=True)),
                ('description', models.TextField(blank=True, help_text='A descriptive summary of the course.', null=True)),
                ('progress', models.IntegerField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['date_added', 'last_updated'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, help_text='When is this section meant to begin.', null=True)),
                ('end_date', models.DateField(blank=True, help_text='When is this section meant to end. Can be left empty', null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Name or Level for this section', max_length=255)),
                ('description', models.TextField(blank=True, help_text='A descriptive summary for this section', null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_added', 'last_updated'],
            },
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, help_text='Describes what this timetable is for', null=True)),
                ('public', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(blank=True, help_text='            If this timetable is for a specific course, fill out this field', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.course')),
                ('section', models.ForeignKey(blank=True, help_text='If this timetable if for a section, fill out this field.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.section')),
            ],
            options={
                'ordering': ['date_added', 'last_updated'],
            },
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of this list', max_length=255)),
                ('description', models.TextField(blank=True, help_text='What is this list for.', null=True)),
                ('public', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_added', 'last_updated'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Topic name, for a course', max_length=255)),
                ('description', models.TextField(blank=True, help_text="Short summary of the topic, or it's meanning", null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='tracker.course')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_added', 'last_updated'],
            },
        ),
        migrations.CreateModel(
            name='TodoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(blank=True, help_text='When does this activity start', null=True)),
                ('end_time', models.TimeField(blank=True, help_text='When does this activity end', null=True)),
                ('activity', models.CharField(help_text='Activity name', max_length=255)),
                ('description', models.TextField(blank=True, help_text='A description of this activity.', null=True)),
                ('day', models.DateField(blank=True, help_text='Day of this activity', null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('todo_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.todo')),
            ],
            options={
                'ordering': ['date_added', 'last_updated'],
            },
        ),
        migrations.CreateModel(
            name='TimeTableActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(help_text='When does this activity start')),
                ('end_time', models.TimeField(help_text='When does this activity end')),
                ('activity', models.CharField(help_text='Activity name', max_length=255)),
                ('description', models.TextField(blank=True, help_text='A description of this activity.', null=True)),
                ('day', models.CharField(choices=[('SUNDAY', 'Sunday'), ('MONDAY', 'Monday'), ('TUESDAY', 'Tuesday'), ('WEDNESDAY', 'Wednesday'), ('THURSDAY', 'Thursday'), ('FRIDAY', 'Friday'), ('SATURDAY', 'Saturday')], help_text='Day for this activity', max_length=10)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('timetable', models.ForeignKey(help_text='What time table does this activity belong to.', on_delete=django.db.models.deletion.CASCADE, related_name='table_items', to='tracker.timetable')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_added', 'last_updated'],
            },
        ),
        migrations.AddField(
            model_name='timetable',
            name='topic',
            field=models.ForeignKey(blank=True, help_text='            If this timetable if for a specific topic, fill out this fiedld', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.topic'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, help_text='A description for this resource.', null=True)),
                ('document', models.FileField(blank=True, help_text='Document resource for a course', null=True, upload_to='uploads/documents', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('link', models.URLField(blank=True, help_text='Url to an online resource, video, document e.t.c', null=True)),
                ('audio', models.FileField(blank=True, help_text='Audio resource like a lecture recording', null=True, upload_to='uploads/audio', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3', 'mtm', 'ec3'])])),
                ('video', models.FileField(blank=True, help_text='Video resource for a course', null=True, storage=cloudinary_storage.storage.VideoMediaCloudinaryStorage, upload_to='uploads/video')),
                ('image', models.ImageField(blank=True, help_text='Image resource for a course.', null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='uploads/images')),
                ('public', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.course')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_added', 'last_updated'],
            },
        ),
        migrations.AddField(
            model_name='course',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='tracker.section'),
        ),
        migrations.AddField(
            model_name='course',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
