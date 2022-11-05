import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from accounts.models import Profile

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("email", "id", "date_joined")


class ProfileType(DjangoObjectType):
    image_url = graphene.String(description="image url")

    class Meta:
        model = Profile
        fields = ('id',)

    def resolve_image_url(self, info):
        return self.get_url()
