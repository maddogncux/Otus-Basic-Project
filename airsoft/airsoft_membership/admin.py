from django.contrib import admin
from .models import BasicGroup, MembershipRequest
# Register your models here.
admin.site.register(BasicGroup)
admin.site.register(MembershipRequest)