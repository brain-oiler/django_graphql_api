import graphene

from accounts.graphql.mutations import AuthMutation
from accounts.graphql.queries import AccountsQuery
from tracker.graphql.queries import TrackerQuery
from tracker.graphql.mutations import TrackerMutation


class Query(TrackerQuery, AccountsQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, TrackerMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
