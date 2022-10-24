import graphene
from graphql import GraphQLError
from graphql_auth.schema import MeQuery
from graphql_auth.schema import UserQuery as not_mine

from .types import UserType


class UserQuery(graphene.ObjectType):
    user = graphene.Field(UserType)

    def resolve_user(self, info, **kwargs):
        if info.context.user.is_anonymous:
            raise GraphQLError("User is not authenticated")
        return info.context.user


class AccountsQuery(UserQuery, not_mine, MeQuery, graphene.ObjectType):
    pass
