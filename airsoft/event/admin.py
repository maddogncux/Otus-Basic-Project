from django.contrib import admin
from typing import TYPE_CHECKING
from .models import Event, EventPost, EventTags
# Register your models here.
if TYPE_CHECKING:
    admin.site: admin.AdminSite

admin.site.register(Event)
admin.site.register(EventPost)
admin.site.register(EventTags)