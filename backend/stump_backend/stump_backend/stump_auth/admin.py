from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import StumpUser

# Register your models here.


class StumpUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2')
            },
        ),
    )

    fieldsets = UserAdmin.fieldsets + (
        (_('Voter information'), {
            'fields': ('language', 'address', 'city', 'state', 'zip_code', 'latitude', 'longitude')
        }),
    )


admin.site.register(StumpUser, StumpUserAdmin)
