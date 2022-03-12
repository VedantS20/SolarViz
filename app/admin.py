# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from atexit import register
from django.contrib import admin
from .models import *

admin.site.register(SolarDBConfig)
    