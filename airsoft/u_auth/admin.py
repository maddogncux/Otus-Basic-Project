# pylint: disable=too-many-ancestors
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from typing import TYPE_CHECKING

from django.contrib import admin

from u_auth.models import UserProfile

# Register your models here.

if TYPE_CHECKING:
    admin.site: admin.AdminSite


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = "pk", "user"
