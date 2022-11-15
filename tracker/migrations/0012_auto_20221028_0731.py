# Generated by Django 3.2.5 on 2022-10-28 07:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0011_auto_20221028_0723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='audio',
            field=models.FileField(blank=True, help_text='Audio resource like a lecture recording', null=True, upload_to='uploads/audio', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3', 'mtm', 'ec3'])]),
        ),
        migrations.AlterField(
            model_name='resource',
            name='document',
            field=models.FileField(blank=True, help_text='Document resource for a course', null=True, upload_to='uploads/documents', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xlsx', 'xls', 'txt'])]),
        ),
        migrations.AlterField(
            model_name='resource',
            name='video',
            field=models.FileField(blank=True, help_text='Video resource for a course', null=True, upload_to='uploads/video', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'wmv', 'avi', 'mkv'])]),
        ),
    ]