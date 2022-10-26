import graphene
# from graphene_django.filter import DjangoFilterConnectionField
from tracker.models import Course, Section, Topic
from .decorators import login_required

from . import types


class TrackerQuery(graphene.ObjectType):
    user_sections = graphene.List(types.SectionType)
    user_courses = graphene.List(types.CourseType)
    user_topics = graphene.List(types.TopicType)

    @login_required
    def resolve_user_sections(root, info, **kwargs):
        return Section.objects.filter(user=info.context.user)

    @login_required
    def resolve_user_courses(root, info, **kwargs):
        return Course.objects.filter(user=info.context.user)

    @login_required
    def resolve_user_topics(root, info, **kwargs):
        return Topic.objects.filter(user=info.context.user)
