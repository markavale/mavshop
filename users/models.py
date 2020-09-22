from django.contrib.auth.models import AbstractUser
from django.db import models
#from .managers import UserManager
# Validation
from django.core.validators import RegexValidator
# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
# import datetime # It could use for computing Age of users


# REGEX FOR STRING COMBINATIONS
USERNAME_REGEX = '^[a-za-z0-9]+$'
CP_NUMBER_REGEX = '^(09|\+639)\d{9}$'
NAME_REGEX = '^[a-zA-Z ]+$'

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))


class User(AbstractUser):
    ip_address      = models.GenericIPAddressField(null=True)
    username = models.CharField(
        max_length=150,
        validators=[
            RegexValidator(regex=USERNAME_REGEX,
                           message='Username must be alphanumeric or contain numbers and lowercaps',
                           code='invalid_username'
                           )],
        unique=True
    )
    image = models.ImageField(default='default.jpg',
                              upload_to='avatar', null=True, blank=True)
    # gender = models.CharField(
    #     max_length=10, blank=True, null=True, choices=GENDER_CHOICES, default="")
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.username

    def get_total_user(self):
        return self.User.objects.all().count()

    def get_user_type(self):
        if self.is_admin:
            return "Admin"
        if self.is_staff:
            return "Staff"
        if self.is_active:
            return "User"

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_first_name(self):
        if self.first_name:
            return self.first_name
        return self.username

    def get_last_name(self):
        if self.last_name:
            return self.last_name
        return self.username

    def has_perm(self, perm, obj=None):  # required
        return True

    def has_module_perms(self, app_label):  # required
        return True

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return '/media/default.jpg'

    # @property
    # def is_admin(self):
    #     return self.admin

    # @property
    # def is_staff(self):
    #     return self.staff

    # @property
    # def is_active(self):
    #     return self.active
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)