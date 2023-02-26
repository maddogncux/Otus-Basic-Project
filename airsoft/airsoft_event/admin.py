from django.contrib import admin

# Register your models here.
from .models import Event,Sides
admin.site.register(Event)
admin.site.register(Sides)
