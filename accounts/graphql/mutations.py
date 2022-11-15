import graphene
from graphql import GraphQLError
from graphql_auth import mutations
from graphene_file_upload.scalars import Upload
from graphql_auth.decorators import login_required
from accounts.models import Profile
from accounts.graphql.types import ProfileType
from graphql_auth.types import ExpectedErrorType


class ProfileCreateUpdateMutation(graphene.Mutation):
    """
    Creates, updates and returns a `Profile` object.
    To perform an update, all you have to do is pass the profile `id`.
    """
    profile = graphene.Field(ProfileType)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    class Arguments:
        profile_id = graphene.ID(
            description="pass this if you want to perform an update.")
        image = Upload(description="The users profile image")

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        profile_id = kwargs.get('profile_id', None)
        if profile_id:
            try:
                profile = Profile.objects.get(pk=profile_id)
                profile.image = kwargs.get('image', profile.image)
                profile.user = info.context.user
                profile.save()
                return ProfileCreateUpdateMutation(
                    profile=profile, success=True)
            except Profile.DoesNotExist:
                raise GraphQLError('The specified profile was not found')
        profile = Profile(
            user=info.context.user,
            image=kwargs.get('image', None))
        profile.save()
        return ProfileCreateUpdateMutation(profile=profile, success=True)


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    verify_token = mutations.VerifyToken.Field()
    verify_account = mutations.VerifyAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    profile_create_update = ProfileCreateUpdateMutation.Field()
