from django.contrib import admin

# Register your models here.
from .models import Organization, OrgRequest, Member

admin.site.register(Organization)
admin.site.register(OrgRequest)
admin.site.register(Member)
