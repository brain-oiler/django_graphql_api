import graphene
from graphql import GraphQLError
# from graphene_django.filter import DjangoFilterConnectionField
from tracker.models import (
    Course, Section,
    Topic, Resource,
    TimeTable, TimeTableActivity,
    Todo)
from .decorators import login_required

from . import types


class TrackerQuery(graphene.ObjectType):
    user_sections = graphene.List(
        types.SectionType,
        description="Resturs all sections created by the logged in user")
    user_courses = graphene.List(
        types.CourseType,
        description="Resturs all courses created by the logged in user")
    get_course_by_id = graphene.Field(
        types.CourseType,
        id=graphene.ID(
            required=True,
            description="The `id` of the target course"),
        description="Returns a course object with the specified `id`.")
    user_topics = graphene.List(
        types.TopicType,
        description="Resturs all topics created by the logged in user")
    user_resources = graphene.List(
        types.ResourceType,
        description="Resturs all topics created by the logged in user")
    get_resources_by_course_id = graphene.List(
        types.ResourceType,
        course_id=graphene.ID(
            required=True,
            description="the course id"),
        description="Returns resources for the course with the specified `id`")
    public_resources = graphene.List(
        types.ResourceType,
        description="Returns all publicly available resources")
    get_user_time_tables = graphene.List(
        types.TimeTableType,
        id=graphene.ID(description="Pass this to filter result by `id`"),
        description="""\
        By default returns all the timetables owned by the logged in user,
        but if as the `id` parameter is passed,
        will filter the resoult by id.""")
    get_time_table_activity_by_id = graphene.Field(
        types.TimeTableActivityType,
        activity_id=graphene.ID(
            required=True, description="`id` of the target activity"),
        description="Returns a `TimeTableActivity` with the specified `id`")
    get_user_todo_list = graphene.List(
        types.TodoType,
        description="Returns a list of todos create by the logged in user")
    get_public_todos = graphene.List(
        types.TodoType,
        description="Returns all public Todo lists")

    @login_required
    def resolve_user_sections(root, info, **kwargs):
        return Section.objects.filter(user=info.context.user)

    @login_required
    def resolve_user_courses(root, info, **kwargs):
        return Course.objects.filter(user=info.context.user)

    @login_required
    def resolve_get_course_by_id(root, info, id, **kwargs):
        try:
            course = Course.objects.get(pk=id)
            if course.user != info.context.user:
                raise GraphQLError(
                    'You are not authorised to view this course')
            return course
        except Course.DoesNotExist:
            return None

    @login_required
    def resolve_user_topics(root, info, **kwargs):
        return Topic.objects.filter(user=info.context.user)

    @login_required
    def resolve_user_resources(root, info, **kwargs):
        return Resource.objects.filter(creator=info.context.user)

    @login_required
    def resolve_get_resources_by_course_id(root, info, course_id, **kwargs):
        try:
            course = Course.objects.get(pk=course_id)
            if not course.user == info.context.user:
                raise GraphQLError(
                    'You are not authorised to perform this action')
            return Resource.objects.filter(course=course)
        except Course.DoesNotExist:
            raise GraphQLError('The specified course was not found')

    @login_required
    def resolve_public_resources(root, info, **kwargs):
        return Resource.objects.filter(public=True)

    @login_required
    def resolve_get_user_time_tables(root, info, **kwargs):
        time_table = TimeTable.objects.filter(user=info.context.user)
        if kwargs.get('id', None):
            return time_table.filter(pk=kwargs.get('id', None))
        return time_table

    @login_required
    def resolve_get_time_table_activity_by_id(root, info, **kwargs):
        try:
            return TimeTableActivity.objects.get(pk=kwargs.get('activity_id'))
        except TimeTableActivity.DoesNotExist:
            raise GraphQLError('The specified activity was not found')

    @login_required
    def resolve_get_user_todo_list(root, info, **kwargs):
        return Todo.objects.filter(user=info.context.user)

    @login_required
    def resolve_get_public_todos(root, info, **kwargs):
        return Todo.objects.filter(public=True)
