import graphene
from django.db.models import Model
from graphene_django import DjangoObjectType

from tracker.models import (
    Course, Section, Topic, Resources, TimeTable, TimeTableActivity,
    Todo, TodoItem)


class SectionType(DjangoObjectType):
    class Meta:
        model: Model = Section
        fields: (str) = (
            "name", "description", "start_date", "end_date", "date_added")


class CourseType(DjangoObjectType):
    class Meta:
        model: Model = Course
        fields: (str) = (
            "name", "start_date", "end_date",
            "description", "section", "progress")


class TopicType(DjangoObjectType):
    class Meta:
        model: Model = Topic
        fields: (str) = (
            "name", "course", "description")


class ResourceType(DjangoObjectType):
    pdf = graphene.String()
    audio = graphene.String()
    image = graphene.String()
    video = graphene.String()

    class Meta:
        model: Model = Resources
        fields: (str) = ("description", "course", "link")

    def resolve_pdf(self, info):
        return self.get_url(self.pdf)

    def resolve_audio(self, info):
        return self.get_url(self.audio)

    def resolve_image(self, info):
        return self.get_url(self.image)

    def resolve_video(self, info):
        return self.get_url(self.video)


class TimeTableType(DjangoObjectType):
    class Meta:
        model: Model = TimeTable
        fields: (str) = ("section", "course", "topic", "description")


class TimeTableActivityType(DjangoObjectType):
    class Meta:
        model: Model = TimeTableActivity
        fields: (str) = (
            "timetable", "start_time", "end_time", "activity",
            "description", "day")


class TodoType(DjangoObjectType):
    class Meta:
        model: Model = Todo
        fields: (str) = ("name", "description")


class TodoItemType(DjangoObjectType):
    class Meta:
        model: Model = TodoItem
        fields: (str) = (
            "start_time", "end_time", "activity", "description", "day")
