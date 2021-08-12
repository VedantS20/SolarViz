from django.contrib import admin
from .models import *
from django.utils.html import format_html


# admin.site.register(Owner)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'firm', 'make', 'color')


class DriverAdmin(admin.ModelAdmin):
    def myphoto(self, obj):
        return format_html('<img src="{}" width="50" />'.format(obj.photo.url))

    list_display = ('id', 'firm', 'first_name', 'myphoto')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'firm')


class AssignAdmin(admin.ModelAdmin):
    list_display = ('id', 'firm', 'device', 'vehicle', 'driver')


admin.site.register(Driver, DriverAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Assign, AssignAdmin)
