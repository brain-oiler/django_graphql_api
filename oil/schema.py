import graphene
from tracker.graphql.queries import TrackeQuery


class Query(TrackeQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
