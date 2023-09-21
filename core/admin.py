from django.contrib import admin
from .models import User, MapLocation, Area, Manufacturer


admin.site.register(User)
admin.site.register(MapLocation)
admin.site.register(Area)
admin.site.register(Manufacturer)
