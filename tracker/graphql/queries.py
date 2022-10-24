import graphene
from graphql_auth.decorators import login_required
# from graphene_django.filter import DjangoFilterConnectionField
from tracker.models import Course, Section

from . import types


class TrackerQuery(graphene.ObjectType):
    user_sections = graphene.Field(types.SectionType)

    @login_required
    def resolve_user_sections(root, info, **kwargs):
        return Section.objects.filter(user=info.context.user)

    def resolve_all_course(root, info, **kwargs):
        return Course.objects.all()
