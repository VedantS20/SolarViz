# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, include  # add this
from . import views

urlpatterns = [
    path('reports/', views.get_report, name='getreport'),
    path('reports/map/', views.get_map_view, name='getmapview'),

]
