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
    path('api/data/report', views.GetReport, name="report"),
    path('api/data/report/map', views.get_map_report, name="report_map"),
    path('api/data/devicelist', views.device_list, name="device_list"),
    path('api/data/deviceparameters', views.device_parameters, name="device_parameters"),
    path('superuser', views.superuser_page, name="superuser"),
    path('api/register/firm', views.firm_register, name="firmregister"),
    path('api/data/tempdevice', views.tempdevice, name="tempdevice"),
    path('api/data/userinfo', views.get_userinfo, name="userinfo"),
    path('api/data/atdata', views.ac_location, name="atlocation"),
    path('api/data/unity', views.unity_api, name="unitydata"),
    path('api/data/power', views.get_solar_genration, name="solargenration"),
    path('api/data/stationreport', views.station_report, name="stationreport"),
    path('api/data/error_code', views.error_code, name="error_code"),
    path('3d', views.show_3d, name="3d"),
    path('api/data/searchtag', views.search_tag, name="searchtag"),
   
    
    re_path(r'^.*\.*', views.pages, name='pages'),
]
