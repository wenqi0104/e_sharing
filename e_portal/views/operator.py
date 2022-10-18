"""
operator用户的所有接口
"""

from django.shortcuts import render,redirect
from django.http import HttpResponse
from .. import models
# Create your views here.


def getUsingVehicles(request):
    """
    被使用的车
    :param request:
    :return: list
    """
    pass


def getUnUsingVehicles(request):
    """
    未使用的车, move:修改经纬度
    :param request:
    :return:
    """
    pass


def getDealVehicles(request):
    """
    需要处理的车,change + repair:broken->available, low battery->available
    :param request:
    :return:
    """
    pass

