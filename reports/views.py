from django.shortcuts import render
from userforms.models import *
from django.contrib.auth.decorators import login_required
from .models import Report
from app.models import *
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.template import loader
from app.operations import getmap


@login_required(login_url="/login/")
def get_report(request):
    driverusernames = []
    ctx = {}
    ctxarr = []
    drivers = User.objects.filter(groups__name__in=['driver'])
    for d in drivers:
        driverusernames.append(d.username)

    if request.user.username in driverusernames:
        driver = Driver.objects.get(user__username=request.user.username)
        driverreport = Report.objects.filter(driver=driver)
        for dr in driverreport:
            ctx = {"TripID": dr.TRIP_ID, "DeviceID": dr.device.device_id, "StartTime": dr.STARTEDT,
                   "EndTime": dr.ENDEDT,
                   "Duration": int(dr.ENDEDT.timestamp() - dr.STARTEDT.timestamp()) / 60,
                   "StartAddress": dr.STARTADDRESS, "EndAddress": dr.ENDADDRESS, "Distance": dr.ENDODO - dr.STARTODO}
            ctxarr.append(ctx)
    else:
        firm = FirmProfile.objects.get(user__username=request.user.username)
        firmreport = Report.objects.filter(firm=firm)
        for fr in firmreport:
            ctx = {"TripID": fr.TRIP_ID, "DeviceID": fr.device.device_id, "StartTime": fr.STARTEDT,
                   "EndTime": fr.ENDEDT,
                   "Duration": int(fr.ENDEDT.timestamp() - fr.STARTEDT.timestamp()) / 60,
                   "StartAddress": fr.STARTADDRESS, "EndAddress": fr.ENDADDRESS, "Distance": fr.ENDODO - fr.STARTODO}
            ctxarr.append(ctx)

    return JsonResponse({"data": ctxarr})


def get_map_view(request):
    context = {}
    if request.method == "POST":
        tripid = request.POST["tripid"]
        deviceid = request.POST["deviceid"]
        report = Report.objects.get(TRIP_ID=tripid, device__device_id=deviceid)
        print(report)
        print(report.STARTEDT)
        print(report.ENDEDT)
        context = {"data": getmap(deviceid, report.STARTEDT, report.ENDEDT)}
        return JsonResponse(context)
    else:
        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))
