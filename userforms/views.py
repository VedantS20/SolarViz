from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *


# Create your views here.

@login_required(login_url="/login/")
def formspage(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        photo = request.POST['photo']
        license_number = request.POST['license']
        aadhar = request.POST['aadhar']
        owner_id = request.POST['owner_id']
        make = request.POST['make']
        model = request.POST['model']
        automatic = request.POST['automatic']
        color = request.POST['color']
        fuel_type = request.POST['fuel_type']
        device_id = request.POST['device_id']
        device_parameters = request.POST['device_parameters']

        if automatic == 'on':
            automatic = True
        else:
            automatic = False

        driver = Driver(first_name=first_name, last_name=last_name, email=email, phone_number=phone, photo=photo,
                        license_number=license_number, aadhar_number=aadhar, owner_id=owner_id)
        vehicle = Vehicle(owner_id=owner_id, make=make, model=model, automatic=automatic, color=color,
                          fuel_type=fuel_type)
        device = Device(owner_id=owner_id, device_id=device_id, device_parameters=device_parameters)

        driver.save()
        vehicle.save()
        device.save()

        return redirect('home')
    return render(request, 'formspage.html')
