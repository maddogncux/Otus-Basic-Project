# pylint: disable=too-many-ancestors
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from django.contrib import admin

from .models import Shop, Member, ShopRequest

# Register your models here.


admin.site.register(Shop)
admin.site.register(Member)
admin.site.register(ShopRequest)
