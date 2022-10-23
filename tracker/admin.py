from django.contrib import admin

from .models import (Section, Course)

# Register your models here.


@admin.register(Section)
class SectionAddmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass
