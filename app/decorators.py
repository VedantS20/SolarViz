from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.models import User


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/login')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = ['driver', 'sysadmin', 'owner', 'newuser']

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            elif group == 'station':
                return redirect('customreports.html')
            elif group == 'solar':
                return redirect('indexsolarmain.html')
            else:
                html_template = loader.get_template('page-403.html')
                return HttpResponse(html_template.render({}, request))

        return wrapper_func

    return decorator


def verified_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = "newuser"

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = []
            if request.user.groups.exists():
                for g in request.user.groups.all():
                    group.append(g.name)
                print(group)

            if allowed_roles not in group:
                return view_func(request, *args, **kwargs)
            else:
                html_template = loader.get_template('page_email_mmverify.html')
                return HttpResponse(html_template.render({}, request))

        return wrapper_func

    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)


def superuser_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff is True:
            return view_func(request, *args, **kwargs)
        else:
            html_template = loader.get_template('page-403.html')
            return HttpResponse(html_template.render({}, request))

    return wrapper_function
