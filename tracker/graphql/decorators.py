from graphql import GraphQLError


def login_required(func):
    def wrapper(root, info, **kwargs):
        if info.context.user.is_anonymous:
            raise GraphQLError(
                'User must be authenticated to perform this action')
        return func(root, info, **kwargs)
    return wrapper
