# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from django.db import connection
from datetime import datetime, timedelta
import pytz
from app.operations import searchdata, getlivedata, getdevicedata, getreport, getmapreport, get_device_parameters, \
    get_all_data, get_livedata_device, get_anchortag, random_string, get_tag, get_solar_column_name, \
    get_livedata_solar, search_solardata, solar_genration, get_live_weatherparam_data, get_tag_location,convert_to_Json
from .decorators import *
from .models import *
from django.contrib.auth.models import User
from userforms.models import *
import os
from django.conf import settings


@login_required(login_url="/login/")
@allowed_users(allowed_roles=['sysadmin', 'owner'])
@verified_users()
def index(request):
    print(request.user.username)
    device = Device.objects.filter(firm=FirmProfile.objects.get(user=User.objects.get(username=request.user.username)))
    get_all_data(device)
    context = {'device': device}
    return render(request, "indexsolar.html", context)


@login_required(login_url="/login/")
def tempdevice(request):
    file = open(os.path.join(settings.BASE_DIR, '../AssetTrack_Backend/log/data.csv'), 'r')
    lines = file.read().splitlines()
    lines.reverse()
    return JsonResponse(lines[0:1000], safe=False)


@login_required(login_url="/login/")
def get_live_data(request):
    arr = []
    dev = []
    weather = []
    if request.user.username == 'solar':
        devicelist = ["SCB1", "SCB2", "SCB3", "inv_1"]
        datalist = get_livedata_solar(devicelist)
        weatherdata = get_live_weatherparam_data()
        for d in devicelist:
            dev.append(get_solar_column_name(d))
        for w in weatherdata:
            weather.append(w)

    else:
        device = Device.objects.filter(
            firm=FirmProfile.objects.get(user=User.objects.get(username=request.user.username)))
        datalist = get_livedata_device(device)
        # print(datalist)

        for k in device:
            dev.append(k.device_parameters.split(","))

    # print(dev)
    # if data is none set device params to None
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
def search_tag(request):
    loc = []
    if request.method == "POST":
        index = 0
        tagid = request.POST["tag"]
        print(tagid)
        tags = TagAssign.objects.all()
        for t in tags:
            loc.append(get_tag("tag_" + t.tag_id))
        for i in range(0, len(tags)):
            if tags[i].tag_id == tagid:
                index = i
        print(loc[index][0], loc[index][1], loc[index][2])
        ctx = {"position": get_tag_location(loc[index][1], loc[index][0], loc[index][2])}
        print(ctx)
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
        # print(param)
        if request.user.username == 'solar':
            device = request.POST.getlist("device[]")
            fromData = fromData.replace(day=23, month=1, year=2021)
            toData = toData.replace(day=23, month=1, year=2021)
            Data = search_solardata(fromData, toData, param, device, weather)
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
                # print(len(Yaxis[0]))
                # print(len(Time))
            

            context = {"fromData": fromData, "toData": toData, "labels": Time, "selected": Yaxis, "param": param1,
                       "legends": params, "yaxislabel": param + weather , "tableData":convert_to_Json(Time,params,Yaxis)}

        else:
            device = request.POST["device"]
            Data = searchdata(fromData, toData, param, device)
            delay = 5
            for _ in range(0, len(param)):
                Yaxis.append([])

            for i in range(0, len(Data) - 2):
                if fromData <= Data[i][0] <= toData:
                    Time.append(Data[i][0].strftime('%Y-%m-%d %H:%M:%S%z'))
                    for j in range(0, len(param)):
                        Yaxis[j].append(Data[i][j + 1])
                    if (Data[i + 1][0] - Data[i][0]) > timedelta(seconds=delay):
                        difference = int(Data[i + 1][0].timestamp() - Data[i][0].timestamp())
                        # print(difference)
                        for sec in range(1, difference):
                            temptimedate = Data[i][0] + timedelta(seconds=delay)
                            Time.append(temptimedate.strftime('%Y-%m-%d %H:%M:%S%z'))
                            for j in range(0, len(param)):
                                Yaxis[j].append(None)
            
            
            context = {"fromData": fromData, "toData": toData, "labels": Time, "selected": Yaxis, "param": param, }
        # edt, vin, vbat, appt, tp, spdk, celv, ect, es = searchdata(fromData, toData,param)

        # while True:
        #     if(fromData > toData):
        #         break
        #     elif(fromData == i.edt):
        #         newtime.append(i.edt.strftime("%H:%M:%S"))
        #         newVin.append(i.vin)
        #     else:
        #         newtime.append(fromData.strftime("%H:%M:%S"))
        #         newVin.append("s")
        #         fromData += timedelta(seconds=1)

        # print(context)
        # print(context.get("Vin"))
        return JsonResponse(context)
    else:
        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def device_list(request):
    context = {"devicelist": getdevicedata()}

    return JsonResponse(context)


@login_required(login_url="/login/")
def device_parameters(request):
    context = {}
    if request.method == "POST":
        context = {"deviceparameters": get_device_parameters(request.POST["deviceid"])}
        return JsonResponse(context)
    else:
        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def GetReport(request):
    context = {"data": getreport()}

    return JsonResponse(context)


@login_required(login_url="/login/")
def get_map_report(request):
    context = {}
    utc = pytz.UTC
    if request.method == "POST":
        tripid = request.POST["tripid"]
        context = {"data": getmapreport(tripid)}
        return JsonResponse(context)
    else:
        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
@superuser_only
def superuser_page(request):
    return render(request, "superuser.html")


@login_required(login_url="/login/")
def ac_location(request):
    loc = []
    id = []
    tag = TagAssign.objects.all()
    for t in tag:
        loc.append(get_tag("tag_" + t.tag_id))
        id.append(t.tag_id)
    # print(loc)

    station_1 = [1, 1.5]
    station_2 = [2, 2.5]
    station_3 = [3, 3.5]
    tag_x = loc[0][0]
    tag_y = loc[0][1]
    tag_z = loc[0][2]
    msg = ""
    shift = ""
    heading = ""
    param = []
    flag = 0
    vin = "XXXXXXX"
    color = "XXXXXXX"
    key_no = "XXXXXX"
    stg = "XXXXXXX"
    use = "XXXXXXX"
    typ = "XXXXXXX"
    station_info = {}
    st_report = StationReport.objects.last()
    if tag_y <= station_1[0]:
        msg = "Vehicle at Entry Point"

    elif station_1[0] <= tag_y <= station_1[1]:
        msg = "Reached Station 1"
        flag = 'station1'

    elif station_1[1] <= tag_y <= station_2[0]:
        msg = "Between Station 1 And Station 2"

    elif station_2[0] <= tag_y <= station_2[1]:
        msg = "Reached Station 2"
        flag = 'station2'

    elif station_2[1] <= tag_y <= station_3[0]:
        msg = "Between Station 2 And Station 3"

    elif station_3[0] <= tag_y <= station_3[1]:
        msg = "Reached Station 3"
        flag = 'station3'

    elif tag_y > station_3[1]:
        msg = "Left Station 3"

    if 7 <= int(datetime.now().strftime("%H")) < 15:
        shift = "A"
    elif 15 <= int(datetime.now().strftime("%H")) < 23:
        shift = "B"
    else:
        shift = "C"

    if request.user.username == flag:
        vin = st_report.vin
        color = "White"
        key_no = "22332233"
        stg = "Power"
        use = "Domestic"
        typ = "City PKP"
    station_info["vin"] = vin
    station_info["color"] = color
    station_info["key_no"] = key_no
    station_info["stg"] = stg
    station_info["use"] = use
    station_info["typ"] = typ

    if request.user.username == 'station1':
        heading = "Trim 1 Intermediate Buy Off"
        param = ['OK', 'NOT OK']
    elif request.user.username == 'station2':
        heading = "Trim 1 Final Buy Off"
        param = ['OK', 'NOT OK']
    elif request.user.username == 'station3':
        heading = "Trim 1 Electrical"
        param = ['OK', 'NOT OK', 'Hazard', 'Cluster indl.', 'Roof lamp', 'Door Switch', 'Central/Key lock',
                 'Regen Switch', 'Wiper Motor', 'HLLD']

    ctx = {"atdata": loc, "tagid": id, "message": msg, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           "shift": shift,
           "heading": heading, "station_info": station_info, "param": param, "flag": flag}
    return JsonResponse(ctx)


def unity_api(request):
    loc = []
    ctx = {}
    tag = TagAssign.objects.all()
    for t in tag:
        loc.append(get_tag("tag_" + t.tag_id))
        if t.tag_id == "54B6":
            ctx["_54B6"] = get_tag("tag_" + t.tag_id)
        else:
            ctx[t.tag_id] = get_tag("tag_" + t.tag_id)
    # print(loc)
    # print(ctx)
    return JsonResponse(ctx)


@login_required(login_url="/login/")
def station_report(request):
    arr = []
    rep = StationReport.objects.all()
    for r in rep.values():
        arr.append(r)
    return JsonResponse({"data": arr})


@login_required(login_url="/login/")
def error_code(request):
    if request.method == 'POST':
        param = request.POST.getlist("params[]")
        vin = request.POST['vin']
        user = request.user.username
        try:
            rep = StationReport.objects.get(vin=vin)
        except:
            msg = "No vehicle available at your station"
        else:
            if len(param) == 0:
                param = "OK"
            else:
                # print(param)
                param = ','.join(param)
            if user == "station1":
                rep.s1_error = param
            elif user == "station2":
                rep.s2_error = param
            elif user == "station3":
                rep.s3_error = param
            rep.save()
            msg = "Saved"
        return JsonResponse({"message": msg})


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
    if request.user.username == 'solar':
        devicelist = ["SCB1", "SCB2", "SCB3", "inv_1"]
        for d in devicelist:
            pref.append(get_solar_column_name(d))
            chart_pref.append(get_solar_column_name(d)[1:])
    else:
        device = Device.objects.filter(
            firm=FirmProfile.objects.get(user=User.objects.get(username=request.user.username)))
        for i in device:
            devicelist.append(i.device_id)
            pref.append(i.device_parameters.split(","))
            chart_pref.append(i.chart_parameters.split(","))
    context = {"all_devices": devicelist, "prefrence": pref, "chartprefrence": chart_pref}
    return JsonResponse(context)


def firm_register(request):
    msg = "Error"
    if request.method == "POST":
        company_name = request.POST["name"]
        company_email = request.POST["email"]
        company_telephone = request.POST["telephone"]
        company_address1 = request.POST["address1"]
        company_address2 = request.POST["address2"]
        company_country = request.POST["country"]
        company_state = request.POST["state"]
        company_city = request.POST["city"]
        company_zip = request.POST["zip"]
        company_gstn = request.POST["gstn"]
        company_owner = request.POST["owner"]
        owner = User.objects.filter(username=company_owner)
        if len(owner) == 0:
            msg = "Owner Not Found"
        elif len(owner[0].groups.filter(name='owner')) == 0:
            msg = "User is not Owner"
        else:
            firm = FirmProfile(user=owner[0], company_name=company_name, company_email=company_email,
                               company_telephone=company_telephone, company_address1=company_address1,
                               company_address2=company_address2,
                               company_country=company_country, company_state=company_state, company_city=company_city,
                               company_zip=company_zip, company_gstn=company_gstn,
                               )
            firm.save()
            msg = "Form Saved Successfully"
        return JsonResponse({'msg': msg})
    else:
        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render({"msg": msg}, request))


def get_solar_genration(request):
    return JsonResponse({"power": solar_genration()})


def show_3d(request):
    return render(request, "unity.html")
