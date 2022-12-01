from django.contrib import admin

# Register your models here.
from airsoft_membership.models import BasicGroup

admin.site.register(BasicGroup)
# admin.site.register(MembershipRequest)