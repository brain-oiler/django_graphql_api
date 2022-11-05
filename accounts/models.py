from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True, blank=False, max_length=254, verbose_name="email address")

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = []


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(
        upload_to="uploads/images", null=True, blank=True)

    def get_url(self, *args, **kwargs):
        if hasattr(self.image, 'url'):
            return self.image.url
        return None
