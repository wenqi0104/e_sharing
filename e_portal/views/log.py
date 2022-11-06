"""
Design all interfaces of login function
Since the three users of the login interface are the same, the views are listed separately.
"""
import json

from django.shortcuts import render, redirect, HttpResponse
from .. import models
from . import globals


# return index page
def index(request):
    if request.method == "GET":
        return render(request, 'pages/index.html')
    else:
        return render(request, 'pages/404.html')


# login page
def login(request):
    globals.user_id = None
    request.session.flush()
    if request.method == "GET":
        return render(request, 'pages/login.html')
    else:  # POST
        name = request.POST.get('name')
        email = request.POST.get('email')  # There is currently no email function for duplicate registration
        pwd = request.POST.get('pwd')
        type = request.POST.get('type')
        if type == "customer":  # 判断用户类型
            all = models.Customers.objects.all()
            for i in all:
                if i.email == email and i.password == pwd:  # If it matches, jump into the index page
                    globals.user_id = i.id
                    request.session['username'] = i.name
                    request.session['avatar'] = json.dumps(str(i.avatar))
                    return redirect("/vehicles")
        elif type == "operator":
            all = models.Operators.objects.all()
            for i in all:
                if i.email == email and i.password == pwd:
                    globals.user_id = i.id
                    request.session['oid'] = i.id
                    request.session['email'] = i.email
                    request.session['username'] = i.name
                    request.session['avatar'] = json.dumps(str(i.avatar))
                    return redirect("operators/vehicles_available/")
        else:
            all = models.Managers.objects.all()
            for i in all:
                if i.email == email and i.password == pwd:
                    globals.user_id = i.id
                    request.session['username'] = i.name
                    request.session['avatar'] = json.dumps(str(i.avatar))
                    return redirect("managers/")
        # If the password or email address is incorrect, enter it again
        return render(request, 'pages/login.html', {'login_error': "email or password error"})


# register page
def register(request):
    if request.method == "GET":
        return render(request, 'pages/register.html')
    else:    # POST
        name = request.POST.get('name')
        # There is currently no email function for duplicate registration
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        if name == "" or email == "" or pwd == "":    # If inputs are empty
            return render(request, 'pages/register.html')
        models.Customers.objects.create(name=name, email=email, password=pwd)
        return redirect("/")


# reset password
def pwd_reset(request):
    if request.method == "GET":
        return render(request, 'pages/pwd_reset.html')
    # else:


# error404
def Error404(request):
    if request.method == "GET":
        all_customers = models.Customers.objects.all()
        for i in all_customers:     # for debug
            print(i.id, i.name, i.password, i.email)  # for debug
        return render(request, 'pages/404.html')
