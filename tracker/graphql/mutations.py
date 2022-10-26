import graphene
from graphql import GraphQLError
from graphql_auth.decorators import login_required
from tracker.models import Section, Course, Topic
from .types import SectionType, CourseType, TopicType


class SectionCreateUpdateMutation(graphene.Mutation):
    """
    Creates, updates and returns a section object. To update all you need to do
    is pass in the section `id` as arguments.
    """
    section = graphene.Field(SectionType)
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID()
        name = graphene.String(
            description="What name would you give this section.")
        description = graphene.String()
        start_date = graphene.Date(description="When does this section begin.")
        end_date = graphene.Date(description="When will this section end.")

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        id = kwargs.get("id", None)
        # if info.context.user.is_anonymous:
        #     raise GraphQLError('User is not authenticated')
        if id:
            try:
                section = Section.objects.get(pk=id)
            except Section.DoesNotExist:
                raise GraphQLError('Specified Section does not exist')
            if section.user == info.context.user:
                section.name = kwargs.get("name", section.name)
                section.description = kwargs.get(
                    "description", section.description)
                section.start_date = kwargs.get(
                    'start_date', section.start_date)
                section.end_date = kwargs.get('end_date', section.end_date)
                section.save()
                return SectionCreateUpdateMutation(
                    section=section, success=True)
            raise GraphQLError(
                'You do not have permissions to update this section')
        section = Section(
            user=info.context.user,
            name=kwargs.get('name', None),
            description=kwargs.get('description', None),
            start_date=kwargs.get('start_date', None),
            end_date=kwargs.get('end_date', None))
        section.save_base()
        return SectionCreateUpdateMutation(section=section, success=True)


class CourseCreateUpdateMutation(graphene.Mutation):
    """
    Creates, updates and returns a course object. To update all
    you need to do is pass the course `id`.
    """
    course = graphene.Field(CourseType)
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID()
        section_id = graphene.ID()
        name = graphene.String()
        description = graphene.String()
        start_date = graphene.Date()
        end_date = graphene.Date()

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        section_id = kwargs.get('section_id', None)
        id = kwargs.get('id', None)
        section = None
        if section_id:
            try:
                section = Section.objects.get(pk=section_id)
                if section.user != info.context.user:
                    raise GraphQLError(
                        'You are not authorised to use this section')
            except Section.DoesNotExist:
                raise GraphQLError('Specified Section was not found')
        if id:
            try:
                course = Course.objects.get(pk=id)
                if course.user != info.context.user:
                    raise GraphQLError(
                        'You are not authorised to edit this course')
                course.name = kwargs.get('name', course.name)
                course.description = kwargs.get(
                    'description', course.description)
                course.start_date = kwargs.get('start_date', course.start_date)
                course.end_date = kwargs.get('end_date', course.end_date)
                course.section = section
                course.save()
                return CourseCreateUpdateMutation(course=course, success=True)
            except Course.DoesNotExist:
                raise GraphQLError('The specified course was not found')
        course = Course(
            name=kwargs.get('name', None),
            description=kwargs.get('description', None),
            end_date=kwargs.get('end_date', None),
            start_date=kwargs.get('start_date', None),
            section=section,
            user=info.context.user)
        course.save()
        return CourseCreateUpdateMutation(course=course, success=True)


class TopicCreateUpdateMutation(graphene.Mutation):
    """
    Creates, updates and returns a `Topic` object for a particular course.
    Note: a course `id` must be passed. To update, all you need to do
    is pass in the topic `id`.
    """
    topic = graphene.Field(TopicType)
    success = graphene.Boolean()

    class Arguments:
        name = graphene.String()
        description = graphene.String()
        topic_id = graphene.ID()
        course_id = graphene.ID(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        try:
            course = Course.objects.get(pk=kwargs.get('course_id'))
            if course.user != info.context.user:
                raise GraphQLError(
                    "You do not have permissions to use this course")
            topic_id = kwargs.get('topic_id', None)
            if topic_id:
                try:
                    topic = Topic.objects.get(pk=topic_id)
                    if topic.user != info.context.user:
                        raise GraphQLError(
                            'You do not have permissions to alter this topic')
                    topic.name = kwargs.get('name', topic.name)
                    topic.description = kwargs.get(
                        'description', topic.description)
                    topic.course = course
                    topic.user = info.context.user
                    topic.save()
                    return TopicCreateUpdateMutation(topic=topic, success=True)
                except Topic.DoesNotExist:
                    raise GraphQLError('The specified topic was not found')
            topic = Topic(
                    name=kwargs.get('name', None),
                    description=kwargs.get('description', None),
                    course=course,
                    user=info.context.user)
            topic.save()
            return TopicCreateUpdateMutation(topic=topic, success=True)
        except Course.DoesNotExist:
            raise GraphQLError('The specified course was not found')


class TrackerMutation(graphene.ObjectType):
    create_update_section = SectionCreateUpdateMutation.Field()
    create_update_course = CourseCreateUpdateMutation.Field()
    create_update_topic = TopicCreateUpdateMutation.Field()