"""
customer用户的所有接口
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .. import models
from . import globals
import django.utils.timezone as timezone


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
    vehicles_available = models.Vehicles.objects.filter(status="available")

    # print(vehicles_list)

    return render(request, "customers/vehicles_list.html", {"vehicles_available": vehicles_available})


# vehicle_details页面返回函数
def getVehicleDetails(request, vid):
    """
    根据前端返回的id，查找特定id的vehicle的信息
    返回这个车的所有信息
    path('/vehicle/vehicle_details/', ... )
    :param vid:
    :param request:
    :return:
    """
    if request.method() == "GET":
        return render(request, 'customers/vehicles_detail.html')
    else:
        details = models.Vehicles.objects.get(vid=vid)
        return render(request, "pages/vehicles_details.html", {"details": details})


def rent(request, vehicles_id):
    uid = globals.user_id
    user = models.Customers.objects.get(id=uid)

    if user.eligible == False:
        return render(request, 'pages/vehicles_details.html',
                      {"error_massage": "Please check if you have an unpaid order or a bike is not returned."})

    # vid = request.PSOT.get('vid')
    # details = models.Vehicles.objects.get(vid=vehicles_id)

    # 创建一个新的订单
    models.Order.objects.create(cid=uid, vid=vehicles_id)

    # unpaid_order = models.Order.objects.filter(cid=uid, status="unpaid")

    # update models
    models.Customers.objects.filter(id=uid).update(elgible=False)
    models.Vehicles.objects.filter(id=vehicles_id).update(status="using")

    msg = "Order created!"

    return redirect(request, 'customers/rents.html', {"message": msg})


def pay(request, order_id):
    order = models.Order.objects.filter(id=order_id)
    order.update(status="paid")

    # 新建Payments表
    models.Payments.objects.create(amount=order.amount, cid=order.cid, vid=order.vid)
    # 更新用户totalSpending
    user = models.Customers.objects.filter(id=order.cid)
    user.update(totalSpending=user.totalSpending + order.amount)

    return redirect('customers/rents.html')


def returnVehicle(request, order_id):
    uid = globals.user_id
    # 把endtime转为datetime形式
    end_time = timezone.now()
    # end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")

    # 拿到order和vehicle信息
    order = models.Order.objects.filter(id=order_id)
    vehicle = models.Vehicles.objects.filter(id=order.vid)

    # 计算费用并修改订单状态
    use_time = (end_time - order.startTime).seconds / 3600 + 1  # 使用时间
    amount = use_time * vehicle.price
    order.update(amount=amount, endTime=end_time)
    # unpaid_order = models.Order.objects.filter(cid=uid, status="unpaid")
    # 修改用户状态
    models.Customers.objects.filter(id=uid).update(eligible=True)
    # 修改车辆状态
    vehicle.update(batteryPercentage=vehicle.batteryPercentage-use_time*10, totalRentalHours=vehicle.totalRentalHours+use_time)
    if vehicle.batteryPercentage <= 20:
        vehicle.update(status="low_battery")
    else:
        vehicle.updates(status="available")

    return redirect(request, 'customers/rents.html')


def report(request, order_id):
    uid = globals.user_id
    # 把endtime转为datetime形式
    end_time = timezone.now()
    # end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")

    # 拿到order和vehicle信息
    order = models.Order.objects.filter(id=order_id)
    vehicle = models.Vehicles.objects.filter(id=order.vid)

    # 计算费用并修改订单状态
    use_time = (end_time - order.startTime).seconds / 3600 + 1  # 使用时间
    amount = use_time * vehicle.price
    order.update(amount=amount, endTime=end_time)
    # 修改用户状态
    models.Customers.objects.filter(id=uid).update(eligible=True)
    # 修改车辆状态为broken
    vehicle.update(status="broken")

    return redirect(request, 'customers/rents.html')


def rents(request):
    """
    GET：
    返回两个对象
    先判断eligible,如果为True：
        1. 目前的正在进行的订单的车辆信息  
        2. 未支付的所有订单
        3. 修改eligible=False
        ### 第一条和第二条没搞懂是需要返回什么
    如果为False：
        返回“你只能租一辆车”
    POST：
    1. 还车：根据时间计算金额，增加未支付订单，返回未支付订单列表
    这一条需要一个计时器（我觉得交前端界面计算比较好）
    2. 故障上报：修改车辆状态，render到主界面，并给出flag（表示是否显示报修弹窗）
    3. 支付单个订单，跳转到支付方式界面
    :param request:
    :return:
    """
    # pass
    uid = globals.user_id
    # user = models.Customers.objects.get(id=uid)

    cur_order = models.Order.objetc.filter(endTime=None)
    unpaid_orders = models.Order.objects.filter(status="unpaid", cid=uid)
    cur_vid = cur_order.vid
    cur_vehicle = models.Vehicles.objects.filter(id=cur_vid)

    return render(request, 'customers/rents.html', {"unpaid_orders": unpaid_orders, "cur_order": cur_order,
                                                    "cur_vehicle": cur_vehicle})


# def payMethod(request): # POST
#     """
#     修改订单状态,返回到index界面，返回未支付的所有订单
#     需要当前订单的id
#     :param request:
#     :return:
#     """


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
    vehicle_all = models.Vehicles.objects.all()
    return render(request, 'pages/index.html', {"vehicle_all":vehicle_all})