"""
设计登录功能的所有接口
由于登录界面三种用户都是一样的，所以单独列出来views
"""

from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .. import models
from . import globals
import django.utils.timezone as timezone

#返回主页
def index(request):
    if request.method == "GET":
        return render(request, 'pages/index.html')
    else:
        return render(request, 'pages/404.html')


# 登录界面
def login(request):
    # add database, only run once
    # models.Order.objects.create(amount="5", status="paid", cid=10, vid=1)
    # models.Order.objects.create(amount=12, cid=8, vid=2)
    globals.user_id = None
    if request.method == "GET":
        return render(request, 'pages/login.html')
    else:  # POST
        name = request.POST.get('name')
        email = request.POST.get('email')  # 暂时没有email判断重复注册的功能
        pwd = request.POST.get('pwd')
        type = request.POST.get('type')
        if type == "customer":  # 判断用户类型
            all = models.Customers.objects.all()
            for i in all:
                if i.email == email and i.password == pwd:  # 如果匹配则进入主界面
                    globals.user_id = i.id
                    request.session['username'] = i.name
                    return redirect("/vehicles")
        elif type == "operator":
            all = models.Operators.objects.all()
            for i in all:
                if i.email == email and i.password == pwd:  # 如果匹配则进入主界面
                    globals.user_id = i.id
                    request.session['oid'] = i.id  # 设置session值
                    request.session['email'] = i.email
                    return redirect("operators/vehicles_available/")
        else:
            all = models.Managers.objects.all()
            for i in all:
                if i.email == email and i.password == pwd:  # 如果匹配则进入主界面
                    globals.user_id = i.id
                    return redirect("manager/")
        return render(request, 'pages/login.html')  # 密码/邮箱错误，则重新输入



#注册界面
def register(request):
    if request.method == "GET":
        return render(request, 'pages/register.html')
    else:    #POST
        name = request.POST.get('name')
        email = request.POST.get('email')  #暂时没有email判断重复注册的功能
        pwd = request.POST.get('pwd')
        if name == "" or email == "" or pwd=="":    #如果为空重新输入
            return render(request, 'pages/register.html')
        # print(name, email, pwd)
        models.Customers.objects.create(name=name, email=email, password=pwd)
        return redirect("/vehicles")

#重置密码
def pwd_reset(request):
    if request.method == "GET":
        return render(request, 'pages/pwd_reset.html')
    # else:


#error404动态
def Error404(request):
    if request.method == "GET":
        all_customers = models.Customers.objects.all()
        for i in all_customers: #for debug
            print(i.id, i.name, i.password, i.email)  #for debug
        return render(request, 'pages/404.html')
