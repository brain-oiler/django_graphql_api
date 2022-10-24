import graphene
from graphql import GraphQLError
from graphql_auth.decorators import login_required
from tracker.models import Section
from .types import SectionType


class SectionCreateUpdateMutation(graphene.Mutation):
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


class TrackerMutation(graphene.ObjectType):
    create_update_section = SectionCreateUpdateMutation.Field()
