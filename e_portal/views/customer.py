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


def getAvailableVehicles(request):
    """
    返回所有可用车辆，不区分e-bike和bike
    可用条件： status == available
    path('/vehicles/', ... )
    :param request:
    :return:
    """
    # vehicles_list = models.Vehicles.objects.all()
    # print(vehicles_list)

    return 0


# vehicle_details页面返回函数
def getVehicleDetails(request):
    """
    根据前端返回的id，查找特定id的vehicle的信息
    返回这个车的所有信息
    path('/vehicle/vehicle_details/', ... )
    :param request:
    :return:
    """
    return 0


def rentToOrder(request):
    """
    GET：
    返回两个对象
    先判断eligible,如果为True：
        1. 目前的正在进行的订单的车辆信息
        2. 未支付的所有订单
        3. 修改eligible=False
    如果为False：
        返回“你只能租一辆车”
    POST：
    1. 还车：根据时间计算金额，增加未支付订单，返回未支付订单列表
    2. 故障上报：修改车辆状态，render到主界面，并给出flag（表示是否显示报修弹窗）
    3. 支付单个订单，跳转到支付方式界面
    :param request:
    :return:
    """
    pass


def payMethod(request):
    """
    修改订单状态,返回到rent界面，返回未支付的所有订单
    :param request:
    :return:
    """
    pass


def consumeBattery(request):
    """
    电量改变
    :param request:
    :return:
    """
    return 0


def showMap(request):
    """
    返回车辆所在经纬度
    :param request:
    :return:
    """
    return 0