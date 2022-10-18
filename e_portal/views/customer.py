"""
customer用户的所有接口
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .. import models


# Create your views here.

def index(request):
    if request.method == "GET":
        return render(request, 'customers/vehicles_list.html')
    else:
        return render(request, 'pages/404.html')
