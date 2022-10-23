import graphene

from tracker.models import Course, Section

from . import types


class TrackeQuery(graphene.ObjectType):
    all_section = graphene.List(types.SectionType)
    all_courses = graphene.List(types.CourseType)

    def resolve_all_section(root, info, **kwargs):
        return Section.objects.all()

    def resolve_all_course(root, info, **kwargs):
        return Course.objects.all()
