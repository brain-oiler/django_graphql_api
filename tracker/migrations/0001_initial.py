# Generated by Django 3.2.5 on 2022-10-17 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Course name', max_length=255)),
                ('start_date', models.DateField(blank=True, help_text='Start date for course. Can be left null.', null=True)),
                ('end_date', models.DateField(blank=True, help_text='End date for course. Can be left null', null=True)),
                ('description', models.TextField(blank=True, help_text='A descriptive summary of the course.', null=True)),
                ('progress', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, help_text='When is this section meant to begin.', null=True)),
                ('end_date', models.DateField(blank=True, help_text='When is this section meant to end. Can be left empty', null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(help_text='Name or Level for this section', max_length=255)),
                ('description', models.TextField(blank=True, help_text='A descriptive summary for this section', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, help_text='Describes what this timetable is for', null=True)),
                ('course', models.ForeignKey(blank=True, help_text='If this timetable is for a specific course, fill out this field', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.course')),
                ('section', models.ForeignKey(blank=True, help_text='If this timetable if for a section, fill out this field.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.section')),
            ],
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of this list', max_length=255)),
                ('description', models.TextField(blank=True, help_text='A short description of this link', null=True)),
            ],
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
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Topic name, for a course', max_length=255)),
                ('description', models.TextField(blank=True, help_text="Short summary of the topic, or it's meanning", null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='tracker.course')),
            ],
        ),
        migrations.CreateModel(
            name='TimeTableActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(help_text='When does this activity start')),
                ('end_time', models.TimeField(help_text='When does this activity end')),
                ('activity', models.CharField(help_text='Activity name', max_length=255)),
                ('description', models.TextField(blank=True, help_text='A description of this activity.', null=True)),
                ('day', models.CharField(choices=[('Su', 'Sunday'), ('Mo', 'Monday'), ('Tu', 'Tuesday'), ('We', 'Wednesday'), ('Th', 'Thursday'), ('Fr', 'Friday'), ('Sa', 'Saturday')], help_text='Day for this activity', max_length=2)),
                ('timetable', models.ForeignKey(help_text='What time table does this activity belong to.', on_delete=django.db.models.deletion.CASCADE, to='tracker.timetable')),
            ],
        ),
        migrations.AddField(
            model_name='timetable',
            name='topic',
            field=models.ForeignKey(blank=True, help_text='If this timetable if for a specific topic, fill out this fiedld', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.topic'),
        ),
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, help_text='A description for this resource.', null=True)),
                ('pdf', models.FileField(blank=True, help_text='Pdf resource for a course', null=True, upload_to='uploads/pdf')),
                ('link', models.URLField(help_text='Url to an online resource, video, document e.t.c')),
                ('audio', models.FileField(blank=True, help_text='Audio resource like a lecture recording', null=True, upload_to='uploads/audio')),
                ('video', models.FileField(help_text='Video resource for a course', upload_to='')),
                ('image', models.ImageField(blank=True, help_text='Image resource for a course.', null=True, upload_to='uploads/images')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.course')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='tracker.section'),
        ),
    ]