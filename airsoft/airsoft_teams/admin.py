from django.contrib import admin
from .models import Team, Team_Member, TeamRequest, TeamPost
# Register your models here.


admin.site.register(Team_Member)
admin.site.register(Team)
admin.site.register(TeamRequest)
admin.site.register(TeamPost)