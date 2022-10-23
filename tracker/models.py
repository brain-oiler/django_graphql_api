from django.db import models

# Create your models here.


class Section(models.Model):
    """
    A study section like a new level or semester.
    """

    start_date = models.DateField(
        help_text="When is this section meant to begin.", null=True, blank=True
    )
    end_date = models.DateField(
        help_text="When is this section meant to end. Can be left empty",
        null=True,
        blank=True,
    )
    date_added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(
        max_length=255, help_text="Name or Level for this section")
    description = models.TextField(
        help_text="A descriptive summary for this section",
        null=True, blank=True
    )


class Course(models.Model):
    """
    A course or subject for a particular section.
    """

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
        Section, on_delete=models.CASCADE, related_name="courses"
    )
    progress = models.IntegerField()


class Topic(models.Model):
    """
    A topic for a particular course.
    """

    name = models.CharField(
        max_length=255, help_text="Topic name, for a course")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="topics")
    description = models.TextField(
        help_text="Short summary of the topic, or it's meanning",
        null=True, blank=True
    )


class Resources(models.Model):
    """
    Study resource (could include video, image, pdf, audio etc)
    could be for a specific course.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField(
        help_text="A description for this resource.", null=True, blank=True
    )
    pdf = models.FileField(
        null=True,
        blank=True,
        upload_to="uploads/pdf",
        help_text="Pdf resource for a course",
    )
    link = models.URLField(
        help_text="Url to an online resource, video, document e.t.c")
    audio = models.FileField(
        null=True,
        blank=True,
        upload_to="uploads/audio",
        help_text="Audio resource like a lecture recording",
    )
    video = models.FileField(help_text="Video resource for a course")
    image = models.ImageField(
        upload_to="uploads/images",
        help_text="Image resource for a course.",
        null=True,
        blank=True,
    )

    def get_url(self, obj):
        if hasattr(obj, 'url'):
            return obj.url
        return None


class TimeTable(models.Model):
    """
    Timetable of any kind (study etc).
    Could be for a particular Section, Course, Topic
    or just a regular timetable
    """
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


DAYS_OF_THE_WEEK = (
    ("Su", "Sunday"),
    ("Mo", "Monday"),
    ("Tu", "Tuesday"),
    ("We", "Wednesday"),
    ("Th", "Thursday"),
    ("Fr", "Friday"),
    ("Sa", "Saturday"),
)


class TimeTableActivity(models.Model):
    """
    Defines an item on the timetable.
    """
    timetable = models.ForeignKey(
        TimeTable,
        on_delete=models.CASCADE,
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
        max_length=2, help_text="Day for this activity",
        choices=DAYS_OF_THE_WEEK
    )


class Todo(models.Model):
    """
    A todo list is a todo list
    """
    name = models.CharField(max_length=255, help_text="Name of this list")
    description = models.TextField(
        null=True, blank=True, help_text="What is this list for."
    )


class TodoItem(models.Model):
    """
    Will describe to a specific item of a todo list.
    """
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
