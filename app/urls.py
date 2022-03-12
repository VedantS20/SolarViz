# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [
    # path('', views.formspage, name='formspage'),
    path('', views.index, name='home'),
    path('api/data/live', views.get_live_data, name='api-data'),
    path('api/data/archive', views.get_archive_data, name="archive"),
    path('api/data/userinfo', views.get_userinfo, name="userinfo"),
    path('solar/testdb', views.solar_db_check, name="solar_check"),
    path('solar/table-list', views.store_table_list, name="solar_check"),
    
   
    
    re_path(r'^.*\.*', views.pages, name='pages'),
]
