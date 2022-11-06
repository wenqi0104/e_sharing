"""
All interfaces for operator users
"""
import json
import math
import random
import time

import geocoder
# from geocoder import arcgis
# from django.core import serializers
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .. import models


class usingItem:
    vid, name, type, cover, color, plateNum, batteryPercentage, lastChargedTime, status, totalRentalHours, locName, latitude, longitude, price, description, oid, amount, status_order, startTime, endTime, cid, address, name_customer, avatar = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

    def __init__(self, vehicles, order, customer):
        self.vid = vehicles.id
        self.name = vehicles.name
        self.type = vehicles.type
        self.cover = vehicles.cover
        self.color = vehicles.color
        self.plateNum = vehicles.plateNum
        self.batteryPercentage = vehicles.batteryPercentage
        self.lastChargedTime = vehicles.lastChargedTime
        self.status = vehicles.status
        self.totalRentalHours = vehicles.totalRentalHours
        self.locName = vehicles.locName
        self.latitude = vehicles.latitude
        self.longitude = vehicles.longitude
        self.price = vehicles.price
        self.description = vehicles.description
        self.oid = order.id
        self.amount = order.amount
        self.status_order = order.status
        self.startTime = order.startTime
        self.endTime = order.endTime
        self.cid = order.cid
        self.address = customer.address
        self.name_customer = customer.name
        self.avatar = customer.avatar


# Create your views here.
# base_log：longitude reference point,
# base_lat：latitude reference point,
# radius：Radius from datum point
def generate_random_gps(base_log=-4.25889, base_lat=55.85806, radius=3000):
    radius_in_degrees = radius / 111300
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)
    longitude = y + base_log
    latitude = x + base_lat
    locName = geocoder.arcgis([latitude, longitude], method='reverse').address
    longitude = '%.10f' % longitude
    latitude = '%.10f' % latitude

    return longitude, latitude, locName
    # data = {"longitude": longitude, "latitude": latitude, "locName": locName}
    # return JsonResponse(data)


def moveVehicles(request):
    # if request.method == "GET":
    #     vid = request.GET.get("vid")
    #     longitude, latitude = generate_random_gps()
    #     models.Vehicles.objects.filter(id=vid).update(longitude=longitude, latitude=latitude)
    #     return HttpResponse("success")

    if request.method == "POST":
        vid = request.POST.get("vid")
        oid = request.session.get('oid')
        longitude, latitude, locName = generate_random_gps()
        models.Vehicles.objects.filter(id=vid).update(longitude=longitude, latitude=latitude, locName=locName)
        models.OperationsHistory.objects.create(operationType='move', oid=oid, vid=vid,
                                                operateTime=time.strftime('%Y-%m-%d %H:%M:%S'))
        data = {"success_msg": "success"}
        return JsonResponse(data)


def getUsingVehicles(request):
    """
    used car
    :param request:
    :return: list
    """
    if request.method == "GET":
        data = models.Vehicles.objects.filter(status="using").all()
        email = request.session.get('email')
        vehicles_using = []
        for vehicles in data:
            order = models.Order.objects.get(vid=vehicles.id, endTime=None)
            user = models.Customers.objects.get(id=order.cid)
            vehicles_using.append(usingItem(vehicles, order, user))
        return render(request, "operator/vehicles_using.html", {"vehicles_using": vehicles_using, "email": email})


def getUnUsingVehicles(request):
    """
    Unused car, move: modify latitude and longitude
    :param request:
    :return:
    """
    if request.method == "GET":
        data = models.Vehicles.objects.filter(status="available").all()
        # data = serializers.serialize('json', data)
        # return HttpResponse(data, content_type="application/json")
        email = request.session.get('email')
        return render(request, "operator/vehicles_available.html", {"vehicles_available": data, "email": email})


def getDealVehicles(request):
    """
    car that needs to be handled,charge + repair:broken->available, low battery->available
    :param request:
    :return:
    """
    if request.method == "GET":
        data_low_battery = models.Vehicles.objects.filter(status="low_battery").all()
        data_broken = models.Vehicles.objects.filter(status="broken").all()
        # data_ex = models.Vehicles.objects.all()
        # vehicles_deal = list(set(data_ex) - set(data_available) - set(data_using))
        return render(request, "operator/vehicles_deal.html", {"vehicles_low_battery": data_low_battery, "vehicles_broken": data_broken})


def usingTrack(request):
    if request.method == "GET":
        data = models.Vehicles.objects.filter(status="using").all()
        return render(request, "operator/vehicles_using_track.html",
                      {"vehicles_using": data})


def availableTrack(request):
    if request.method == "GET":
        data_lb = models.Vehicles.objects.filter(status="low_battery").all()
        data_broken = models.Vehicles.objects.filter(status="broken").all()
        data_ex = models.Vehicles.objects.all()
        vehicles_available = list(set(data_ex) - set(data_lb) - set(data_broken))
        return render(request, "operator/vehicles_available_track.html", {"vehicles_available": vehicles_available})


def dealTrack(request):
    if request.method == "GET":
        data_available = models.Vehicles.objects.filter(status="available").all()
        data_using = models.Vehicles.objects.filter(status="using").all()
        data_ex = models.Vehicles.objects.all()
        data = list(set(data_ex) - set(data_available) - set(data_using))
        return render(request, "operator/vehicles_deal_track.html", {"vehicles_deal": data})


def chargeVehicles(request):
    if request.method == "POST":
        apply_type = "charge"
        vid = request.POST.get("vid")
        oid = request.session.get('oid')
        models.Vehicles.objects.filter(id=vid).update(status="available", batteryPercentage=100)
        models.OperationsHistory.objects.create(operationType=apply_type, oid=oid, vid=vid,
                                                operateTime=time.strftime('%Y-%m-%d %H:%M:%S'))
        data = {"success_msg": "success"}
        return JsonResponse(data)


def chargeBrokenVehicles(request):
    if request.method == "POST":
        apply_type = "charge"
        vid = request.POST.get("vid")
        oid = request.session.get('oid')
        models.Vehicles.objects.filter(id=vid).update(batteryPercentage=100)
        models.OperationsHistory.objects.create(operationType=apply_type, oid=oid, vid=vid,
                                                operateTime=time.strftime('%Y-%m-%d %H:%M:%S'))
        data = {"success_msg": "success"}
        return JsonResponse(data)


def repairVehicles(request):
    if request.method == "POST":
        apply_type = "repair"
        vid = request.POST.get("vid")
        locName = request.POST.get("locName")
        oid = request.session.get('oid')
        models.Vehicles.objects.filter(id=vid).update(status="available")
        models.OperationsHistory.objects.create(operationType=apply_type, oid=oid, vid=vid,
                                                operateTime=time.strftime('%Y-%m-%d %H:%M:%S'))
        models.RepairHistory.objects.create(repairedLoc=locName, oid=oid, vid=vid,
                                            repairedTime=time.strftime('%Y-%m-%d %H:%M:%S'))
        data = {"success_msg": "success"}
        return JsonResponse(data)


def getOperator():
    oid = requests.Session.get('oid')
    email = requests.Session.get('email')
    data = {"success_msg": "success", "oid": oid, "email": email}
    return JsonResponse(data)


def track(request):
    brokens = models.Vehicles.objects.filter(status="available")
    low_batterys = models.Vehicles.objects.filter(status="low_battery")
    availables = models.Vehicles.objects.filter(status="available")
    usings = models.Vehicles.objects.filter(status="using")

    return render(request, "/operator/track.html", {"brokens": brokens, "low_batterys": low_batterys,
                                                    "availables": availables, "usings": usings})


def getVehicleDetails(request, vehicles_id):
    """
    According to the id returned by the front end, find the information of the vehicle with a specific id
    Return all information about this car
    path('/vehicle/vehicle_details/', ... )
    :param vid:
    :param request:
    :return:
    """
    details = models.Vehicles.objects.get(id=vehicles_id)
    return render(request, "operator/vehicle_detail.html", {"details": details})
