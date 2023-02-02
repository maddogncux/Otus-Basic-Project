from django.contrib import admin
from typing import TYPE_CHECKING
from u_auth.models import UserProfile

# Register your models here.

if TYPE_CHECKING:
    admin.site: admin.AdminSite

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = "pk", "user"
