from django.contrib import admin
from typing import TYPE_CHECKING
from .models import (Event,
                     EventPost,
                     EventTags,
                     EventReg,
                     AdditionalServices,
                     Sides,
                     RegisteredTeams,
                     )
# Register your models here.
if TYPE_CHECKING:
    admin.site: admin.AdminSite

class TeamsAdmin(admin.ModelAdmin):
    list_display = ("name", "city")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Event,)
admin.site.register(EventPost)
admin.site.register(EventTags)
admin.site.register(EventReg)
admin.site.register(AdditionalServices)
admin.site.register(Sides)
admin.site.register(RegisteredTeams)