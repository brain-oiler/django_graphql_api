import graphene
from django.db.models import Model
from graphene_django import DjangoObjectType

from tracker.models import (
    Course, Section, Topic, Resource, TimeTable, TimeTableActivity,
    Todo, TodoItem)


class SectionType(DjangoObjectType):
    class Meta:
        model: Model = Section
        fields: (str) = (
            "name", "description", "start_date", "end_date",
            "date_added", "id")
        filter_fields = {
            'start_date': ['exact'],
            'end_date': ['exact'],
            'name': ['exact', 'icontatins', 'istartswith']
        }
        interface = (graphene.relay.Node, )


class CourseType(DjangoObjectType):
    class Meta:
        model: Model = Course
        fields: (str) = (
            "name", "start_date", "end_date",
            "description", "section", "progress", "id")
        filter_fields = {
            'start_date': ['exact'],
            'end_date': ['exact'],
            'name': ['exact', 'icontatins', 'istartswith']
        }
        interface = (graphene.relay.Node, )


class TopicType(DjangoObjectType):
    class Meta:
        model: Model = Topic
        fields: (str) = (
            "name", "course", "description", "id")
        filter_fields = {
            'course': ['exact'],
            'name': ['exact', 'icontatins', 'istartswith']
        }
        interface = (graphene.relay.Node, )


class ResourceType(DjangoObjectType):
    pdf = graphene.String()
    audio = graphene.String()
    image = graphene.String()
    video = graphene.String()

    class Meta:
        model: Model = Resource
        fields: (str) = ("creator", "description", "course", "link")
        filter_fields = {
            'creator': ['exact'],
            'course': ['exact'],
            'description': ['exact', 'icontatins', 'istartswith']
        }
        interface = (graphene.relay.Node, )

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
        filter_fields = {
            'section': ['exact'],
            'course': ['exact'],
            'topic': ['exact', 'icontatins', 'istartswith']
        }
        interface = (graphene.relay.Node, )


class TimeTableActivityType(DjangoObjectType):
    class Meta:
        model: Model = TimeTableActivity
        fields: (str) = (
            "timetable", "start_time", "end_time", "activity",
            "description", "day")
        filter_fields = {
            'activity': ['exact', 'icontatins', 'istartswith'],
            'description': ['exact', 'icontatins', 'istartswith']
        }
        interface = (graphene.relay.Node, )


class TodoType(DjangoObjectType):
    class Meta:
        model: Model = Todo
        fields: (str) = ("name", "description")
        filter_fields = {
            'name': ['exact', 'icontatins', 'istartswith'],
            'description': ['exact', 'icontatins', 'istartswith']
        }
        interface = (graphene.relay.Node, )


class TodoItemType(DjangoObjectType):
    class Meta:
        model: Model = TodoItem
        fields: (str) = (
            "start_time", "end_time", "activity", "description", "day")
        filter_fields = {
            'activity': ['exact', 'icontatins', 'istartswith'],
            'description': ['exact', 'icontatins', 'istartswith'],
            'day': ['exact'],
            'start_date': ['exact'],
            'end_date': ['exact']
        }
        interface = (graphene.relay.Node, )
