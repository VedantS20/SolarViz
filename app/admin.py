# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from atexit import register
from django.contrib import admin
from .models import *


class TagAssignAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'vin', 'station_pos')


admin.site.register(UserProfile)
admin.site.register(FirmProfile)
admin.site.register(StationReport)
admin.site.register(TagAssign, TagAssignAdmin)
admin.site.register(SolarDBConfig)
    