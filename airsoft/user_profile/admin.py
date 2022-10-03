from typing import TYPE_CHECKING
from django.contrib import admin
from .models import Player

if TYPE_CHECKING:
    admin.site: admin.AdminSite

# Register your models here.

admin.site.register(Player)
