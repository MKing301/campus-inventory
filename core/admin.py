from django.contrib import admin
from .models import (
    User,
    MapLocation,
    Area,
    Manufacturer,
    InventoryItem,
    ApprovalList,
    Assignee,
    ItemStatus
    )


admin.site.register(User)
admin.site.register(MapLocation)
admin.site.register(Area)
admin.site.register(Manufacturer)
admin.site.register(InventoryItem)
admin.site.register(ApprovalList)
admin.site.register(Assignee)
admin.site.register(ItemStatus)
