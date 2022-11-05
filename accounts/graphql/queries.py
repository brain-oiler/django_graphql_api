import graphene
from graphql import GraphQLError
from graphql_auth.schema import MeQuery
from graphql_auth.schema import UserQuery as not_mine
from accounts.models import Profile
from .types import UserType, ProfileType


class UserQuery(graphene.ObjectType):
    user = graphene.Field(UserType)
    profile = graphene.Field(ProfileType)

    def resolve_user(self, info, **kwargs):
        if info.context.user.is_anonymous:
            raise GraphQLError("User is not authenticated")
        return info.context.user

    def resolve_profile(self, info, **kwargs):
        return Profile.objects.get(user=info.context.user)


class AccountsQuery(UserQuery, not_mine, MeQuery, graphene.ObjectType):
    pass
