"""
operator用户的所有接口
"""
import json
import math
import random
import time

from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .. import models


# Create your views here.

def generate_random_gps(base_log=102.7, base_lat=25, radius=1000000):
    radius_in_degrees = radius / 111300
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)
    longitude = y + base_log
    latitude = x + base_lat
    longitude = '%.2f' % longitude
    latitude = '%.2f' % latitude
    return longitude, latitude


def moveVehicles(request):
    # if request.method == "GET":
    #     vid = request.GET.get("vid")
    #     longitude, latitude = generate_random_gps()
    #     models.Vehicles.objects.filter(id=vid).update(longitude=longitude, latitude=latitude)
    #     return HttpResponse("success")

    if request.method == "POST":
        vid = request.POST.get("vid")
        oid = request.session.get('oid')
        longitude, latitude = generate_random_gps()
        models.Vehicles.objects.filter(id=vid).update(longitude=longitude, latitude=latitude)
        models.OperationsHistory.objects.create(operationType='move', oid=oid, vid=vid, operateTime=time.strftime('%Y-%m-%d %H:%M:%S'))
        data = {"success_msg": "success"}
        return JsonResponse(data)


def getUsingVehicles(request):
    """
    被使用的车
    :param request:
    :return: list
    """
    if request.method == "GET":
        data = models.Vehicles.objects.filter(status="using").all()
        # data = serializers.serialize('json', data)
        # return HttpResponse(data, content_type="application/json")
        return render(request, "operator/vehicles_using.html", {"vehicles_using": data})


def getUnUsingVehicles(request):
    """
    未使用的车, move:修改经纬度
    :param request:
    :return:
    """
    if request.method == "GET":
        data = models.Vehicles.objects.filter(status="available").all()
        # data = serializers.serialize('json', data)
        # return HttpResponse(data, content_type="application/json")
        return render(request, "operator/vehicles_available.html", {"vehicles_available": data})


def getDealVehicles(request):
    """
    需要处理的车,charge + repair:broken->available, low battery->available
    :param request:
    :return:
    """
    if request.method == "GET":
        data_available = models.Vehicles.objects.filter(status="available").all()
        data_ex = models.Vehicles.objects.all()
        vehicles_deal = list(set(data_ex) - set(data_available))
        return render(request, "operator/vehicles_deal.html", {"vehicles_deal": vehicles_deal})


def chargeVehicles(request):
    if request.method == "POST":
        apply_type = "charge"
        vid = request.POST.get("vid")
        oid = request.session.get('oid')
        models.Vehicles.objects.filter(id=vid).update(status="available", batteryPercentage=100)
        models.OperationsHistory.objects.create(operationType=apply_type, oid=oid, vid=vid, operateTime=time.strftime('%Y-%m-%d %H:%M:%S'))
        data = {"success_msg": "success"}
        return JsonResponse(data)


def repairVehicles(request):
    if request.method == "POST":
        apply_type = "repair"
        vid = request.POST.get("vid")
        locName = request.POST.get("locName")
        oid = request.session.get('oid')
        models.Vehicles.objects.filter(id=vid).update(status="available")
        models.OperationsHistory.objects.create(operationType=apply_type, oid=oid, vid=vid, operateTime=time.strftime('%Y-%m-%d %H:%M:%S'))
        models.RepairHistory.objects.create(repairedLoc=locName, oid=oid, vid=vid, repairedTime=time.strftime('%Y-%m-%d %H:%M:%S'))
        data = {"success_msg": "success"}
        return JsonResponse(data)
