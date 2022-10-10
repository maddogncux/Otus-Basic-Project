from django.contrib import admin
from typing import TYPE_CHECKING, List, Any
from .models import Teams, MemberRequests
# from django.contrib.auth.admin import UserAdmin
# from .models import User
# Register your models here.

if TYPE_CHECKING:
    admin.site: admin.AdminSite



class TeamsAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "city", "member_list","member","members")
    prepopulated_fields = {"slug": ("name",)}
#     inlines = MembersInline
#
# class MembersInline(admin.TabularInline):
#     model = Members


# admin.site.register(User, UserAdmin)
admin.site.register(Teams)
# admin.site.register(MemberLists)
# admin.site.register(RequestLists)
# admin.site.register(Members)
admin.site.register(MemberRequests)