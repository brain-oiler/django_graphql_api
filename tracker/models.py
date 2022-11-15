from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from cloudinary_storage.validators import validate_video
from cloudinary_storage.storage import (
    MediaCloudinaryStorage,
    VideoMediaCloudinaryStorage)
# Create your models here.

User = get_user_model()


class Section(models.Model):
    """
    A study section like a new level or semester.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(
        help_text="When is this section meant to begin.", null=True, blank=True
    )
    end_date = models.DateField(
        help_text="When is this section meant to end. Can be left empty",
        null=True,
        blank=True,
    )
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(
        max_length=255, help_text="Name or Level for this section")
    description = models.TextField(
        help_text="A descriptive summary for this section",
        null=True, blank=True
    )

    class Meta:
        ordering = ['date_added', 'last_updated']


class Course(models.Model):
    """
    A course or subject this might be for a particular section.
    """

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, help_text="Course name")
    start_date = models.DateField(
        help_text="When will the user start taking this course",
        null=True, blank=True
    )
    end_date = models.DateField(
        help_text="End date for course. Can be left null",
        null=True, blank=True
    )
    description = models.TextField(
        help_text="A descriptive summary of the course.", null=True, blank=True
    )
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="courses",
        null=True, blank=True
    )
    progress = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_added', 'last_updated']


class Topic(models.Model):
    """
    A topic for a particular course.
    """

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(
        max_length=255, help_text="Topic name, for a course")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="topics")
    description = models.TextField(
        help_text="Short summary of the topic, or it's meanning",
        null=True, blank=True
    )
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_added', 'last_updated']


class Resource(models.Model):
    """
    Study resource (could include video, image, pdf, audio etc)
    could be for a specific course.
    """
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField(
        help_text="A description for this resource.", null=True, blank=True
    )
    document = models.FileField(
        null=True,
        blank=True,
        validators=[FileExtensionValidator(
            allowed_extensions=[
                'pdf'])],
        upload_to="uploads/documents",
        help_text="Document resource for a course",
    )
    link = models.URLField(
        help_text="Url to an online resource, video, document e.t.c",
        null=True, blank=True)
    audio = models.FileField(
        null=True,
        blank=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['mp3', 'mtm', 'ec3'])],
        upload_to="uploads/audio",
        help_text="Audio resource like a lecture recording",
    )
    video = models.FileField(
        null=True,
        blank=True,
        storage=VideoMediaCloudinaryStorage,
        validators=[validate_video],
        upload_to="uploads/video",
        help_text="Video resource for a course")
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="uploads/images",
        help_text="Image resource for a course.",
        null=True,
        blank=True,
    )
    public = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_added', 'last_updated']

    def get_url(self, obj):
        if obj and hasattr(obj, 'url'):
            return obj.url
        return None


class TimeTable(models.Model):
    """
    Timetable of any kind (study etc).
    Could be for a particular Section, Course, Topic
    or just a regular timetable
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(
        Section,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="If this timetable if for a section, fill out this field.",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="\
            If this timetable is for a specific course, fill out this field",
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="\
            If this timetable if for a specific topic, fill out this fiedld",
    )
    description = models.TextField(
        help_text="Describes what this timetable is for", null=True, blank=True
    )
    public = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_added', 'last_updated']


class TimeTableActivity(models.Model):
    """
    Defines an item on the timetable.
    """
    class DaysOfTheWeek(models.TextChoices):
        Sunday = 'SUNDAY'
        Monday = 'MONDAY'
        Tuesday = 'TUESDAY'
        Wednesday = 'WEDNESDAY'
        Thursday = 'THURSDAY'
        Friday = 'FRIDAY'
        Saturday = 'SATURDAY'
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timetable = models.ForeignKey(
        TimeTable,
        on_delete=models.CASCADE,
        related_name="table_items",
        help_text="What time table does this activity belong to.",
    )
    start_time = models.TimeField(
        help_text="When does this activity start",
    )
    end_time = models.TimeField(help_text="When does this activity end")
    activity = models.CharField(max_length=255, help_text="Activity name")
    description = models.TextField(
        help_text="A description of this activity.", null=True, blank=True
    )
    day = models.CharField(
        max_length=10, help_text="Day for this activity",
        choices=DaysOfTheWeek.choices
    )
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_added', 'last_updated']


class Todo(models.Model):
    """
    A todo list is a todo list
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, help_text="Name of this list")
    description = models.TextField(
        null=True, blank=True, help_text="What is this list for."
    )
    public = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_added', 'last_updated']


class TodoItem(models.Model):
    """
    Will describe to a specific item of a todo list.
    """
    todo_list = models.ForeignKey(Todo, on_delete=models.CASCADE)
    start_time = models.TimeField(
        help_text="When does this activity start", null=True, blank=True
    )
    end_time = models.TimeField(
        help_text="When does this activity end", null=True, blank=True
    )
    activity = models.CharField(max_length=255, help_text="Activity name")
    description = models.TextField(
        help_text="A description of this activity.", null=True, blank=True
    )
    day = models.DateField(
        help_text="Day of this activity", null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_added', 'last_updated']
