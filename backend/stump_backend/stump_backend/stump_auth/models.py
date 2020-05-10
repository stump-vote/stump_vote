from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import ugettext_lazy as _

from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USStateField, USZipCodeField

# Create your models here.

class StumpUserManager(UserManager):

    def create_user(self, username, email, password=None):
        return super(StumpUserManager).create_user(username, email, password)


class StumpUser(AbstractUser):
    # password: use default implementation from superclass
    # last_login: use default implementation from superclass
    # username: use default implementation from superclass
    # first_name: use default implementation from superclass
    # last_name: use default implementation from superclass
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        })
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # is_staff: use default implementation from superclass
    # is_active: use default implementation from superclass
    # date_joined: use default implementation from superclass

    objects = StumpUserManager()

    # Stump voter location fields
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = USStateField(choices=STATE_CHOICES)
    zip_code = USZipCodeField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
