from django.contrib import admin
from typing import TYPE_CHECKING
from .models import Organizations

# Register your models here.

# Register your models here.
if TYPE_CHECKING:
    admin.site: admin.AdminSite


class TeamsAdmin(admin.ModelAdmin):
    list_display = ("name", "city")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Organizations)
