# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm, UserProfileForm
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from .tokens import account_activation_token
from django.template.loader import get_template
from app.models import UserProfile, FirmProfile
from app.operations import get_all_data

UserModel = get_user_model()


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            profileobj = ""
            userobj = User.objects.filter(username=username)
            if len(userobj) != 0:
                profileobj = UserProfile.objects.get(user=userobj[0])
            if user is not None:
                login(request, user)
                return redirect("/")
            elif len(userobj) == 0:
                msg = 'Invalid credentials'
            elif userobj[0].check_password(password) is False:
                msg = 'Invalid credentials'
            elif profileobj.email_is_verified is False:
                msg = 'Email is not verified'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            userform = form.save()
            profile = profile_form.save(commit=False)
            profile.user = userform
            group = Group.objects.get(name=profile_form.cleaned_data.get('usertype'))
            group1 = Group.objects.get(name='newuser')
            userform.is_active = False
            userform.save()
            profile.save()
            userform.groups.add(group)
            userform.groups.add(group1)
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")

            # user = authenticate(username=username, password=raw_password)
            msg = 'User created - please <a href="/login">login</a>.'
            success = True
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            template = get_template('acc_activation.html')
            html_content = template.render({
                'user': userform,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(userform.pk)),
                'token': default_token_generator.make_token(userform),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMultiAlternatives(
                mail_subject, to=[to_email]
            )
            email.attach_alternative(html_content, 'text/html')
            email.send()

            html_template = loader.get_template('page_email_verify.html')
            return HttpResponse(html_template.render({}, request))
            # return HttpResponse('Please confirm your email address to complete the registration')

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
        profile_form = UserProfileForm()

    return render(request, "accounts/register.html",
                  {"form": form, "profile_form": profile_form, "msg": msg, "success": success})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        userobj = UserProfile.objects.get(user=user)
        userobj.email_is_verified = True
        userobj.save()
        user.save()

        html_template = loader.get_template('page_email_verified.html')
        return HttpResponse(html_template.render({}, request))
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        html_template = loader.get_template('page_email_invalid.html')
        return HttpResponse(html_template.render({}, request))
