# pylint: disable=too-many-ancestors
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from django.contrib import admin

from .models import Team, TeamMember, TeamRequest, TeamPost

# Register your models here.


admin.site.register(TeamMember)
admin.site.register(Team)
admin.site.register(TeamRequest)
admin.site.register(TeamPost)
