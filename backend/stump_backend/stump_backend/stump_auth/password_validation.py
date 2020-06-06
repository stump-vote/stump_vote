from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import check_password

class PasswordSameAsOldValidator:

    def __init__(self):
        pass

    def validate(self, password, user=None):
        if user is not None and check_password(password, user.password):
            raise ValidationError(_("New password cannot be the same as the old password"), code='password_same_as_old')

    def get_help_text(self):
        return _("New password cannot be the same as the old password")
