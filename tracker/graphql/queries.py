import graphene
# from graphene_django.filter import DjangoFilterConnectionField
from tracker.models import Course, Section
from .decorators import login_required

from . import types


class TrackerQuery(graphene.ObjectType):
    user_sections = graphene.List(types.SectionType)

    @login_required
    def resolve_user_sections(root, info, **kwargs):
        return Section.objects.filter(user=info.context.user)

    def resolve_all_course(root, info, **kwargs):
        return Course.objects.all()
