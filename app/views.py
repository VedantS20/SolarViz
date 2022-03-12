# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from distutils.command.config import config
from email import message
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from django.db import connection
from datetime import datetime, timedelta
import pytz
from app.operations import get_solar_column_name, get_livedata_solar, search_solardata, solar_genration, get_live_weatherparam_data,convert_to_Json,connectToDB
from .decorators import *
from .models import *
from django.contrib.auth.models import User 
import os
import ast
from django.conf import settings



# @allowed_users(allowed_roles=['sysadmin', 'owner'])
# @verified_users()
@login_required(login_url="/login/")
def index(request):
  

    devicelist = ast.literal_eval(SolarDBConfig.objects.get().selectedTables)
    context = {"devicelist":devicelist}
    return render(request, "indexsolarmain.html", context)



@login_required(login_url="/login/")
def get_live_data(request):
    arr = []
    dev = []
    weather = []
    devicelist = ["mvps1_inv_a","mvps4_inv_b","mvps5_inv_a","mvps5_inv_b","mvps6_inv_b","mvps6_inv_a","mvps7_inv_a","mvps7_inv_b"]
    datalist = get_livedata_solar(devicelist)
    weatherdata = get_live_weatherparam_data()
    for d in devicelist:
        dev.append(get_solar_column_name(d))
    for w in weatherdata:
        weather.append(w)

    for i in range(0, len(dev)):
        # dev = device[i].device_parameters.split(",")
        x = {}
        for j in range(0, len(dev[i])):
            if datalist[i] is None:
                x[dev[i][j]] = None
            else:
                x[dev[i][j]] = datalist[i][j]
        arr.append(x)
    ctx = {"data": arr, "weather": weather}
    return JsonResponse(ctx)




@login_required(login_url="/login/")
def get_archive_data(request):
    context = {}
    utc = pytz.UTC
    if request.method == "POST":
        Time = []
        Yaxis = []
        delay = 0
        fromData = (datetime.strptime(request.POST["from"], '%Y-%m-%d %H:%M:%S'))
        toData = (datetime.strptime(request.POST["to"], '%Y-%m-%d %H:%M:%S'))
        param = request.POST.getlist("parameters[]")
        weather = request.POST.getlist("weather[]")
        device = request.POST.getlist("device[]")
        SolarData = SolarDBConfig.objects.get()
        config = {}
        config['user'] = SolarData.user
        config['host'] = SolarData.host
        config['database'] = SolarData.database
        config['password'] = SolarData.password
        Data = search_solardata(config,fromData, toData, param, device, weather)
        delay = 300
        param1 = []
        params = []
        end = len(param)
        for d in device:
            for p in param:
                params.append(f"{d} - {p}")
                param1.append(p)
        for w in weather:
            params.append(w)

        param1.extend(weather)
        for data in Data:
            yaxis = []
            time = []

            if Data.index(data) > len(device) - 1:
                end = len(weather)

            for _ in range(0, end):
                yaxis.append([])
            for i in range(0, len(data) - 2):
                if fromData <= data[i][0] <= toData:
                    time.append(data[i][0].strftime('%Y-%m-%d %H:%M:%S%z'))
                    for j in range(0, end):
                        yaxis[j].append(data[i][j + 1])
                    if (data[i + 1][0] - data[i][0]) > timedelta(seconds=delay):
                        difference = int(data[i + 1][0].timestamp() - data[i][0].timestamp())

                        # print(difference)
                        for sec in range(1, difference):
                            temptimedate = data[i][0] + timedelta(seconds=delay)
                            time.append(temptimedate.strftime('%Y-%m-%d %H:%M:%S%z'))
                            for j in range(0, end):
                                yaxis[j].append(None)

            Yaxis.extend(yaxis)
            Time = time
                
            

        context = {"fromData": fromData, "toData": toData, "labels": Time, "selected": Yaxis, "param": param1,
                       "legends": params, "yaxislabel": param + weather , "tableData":convert_to_Json(Time,params,Yaxis)}

        return JsonResponse(context)
    else:
        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))









@login_required(login_url="/login/")
def pages(request):
    context = {"1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        html_template = loader.get_template(load_template)

        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def get_userinfo(request):
    devicelist = []
    pref = []
    chart_pref = []
    SolarData = SolarDBConfig.objects.get()
    devicelist = ast.literal_eval(SolarData.selectedTables)
    config = {}
    config['user'] = SolarData.user
    config['host'] = SolarData.host
    config['database'] = SolarData.database
    config['password'] = SolarData.password
    # devicelist = ["mvps1_inv_a","mvps4_inv_b","mvps5_inv_a","mvps5_inv_b","mvps6_inv_a","mvps6_inv_b","mvps7_inv_a","mvps7_inv_b"]
    for d in devicelist:
        pref.append(get_solar_column_name(config,d))
        chart_pref.append(get_solar_column_name(config,d)[1:])

    context = {"all_devices": devicelist, "prefrence": pref, "chartprefrence": chart_pref}
    return JsonResponse(context)


@login_required(login_url="/login/")
def solar_db_check(request):
    if request.method == 'POST':
        config = {}
        print(request.POST['user'])
        print(request.POST['database'])
        print(request.POST['host'])
        print(request.POST['password'])
        config['user'] = request.POST['user']
        config['host'] = request.POST['host']
        config['database'] = request.POST['database']
        config['password'] = request.POST['password']
        res = connectToDB(config)
        
        return JsonResponse(res)


@login_required(login_url="/login/")
def store_table_list(request):
    if request.method == 'POST':
        t = request.POST.getlist('checkedTables[]')
        user = request.POST['user']
        host = request.POST['host']
        database = request.POST['database']
        password = request.POST['password']
       
        message = ''
        if(len(t)!=0):
            tables = SolarDBConfig(selectedTables=t,host=host,user = user,database=database,password=password)
            tables.save()
            message = "Table List Saved Succesfully !"
        else:
            message = "Cannot Save Empty Table List !"
        return JsonResponse({"message":message})

