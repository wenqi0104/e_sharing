"""
customer用户的所有接口
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .. import models
from . import globals
import django.utils.timezone as timezone
from django.urls import reverse


class RentsItems:
    oid, v_type, plate_num, start_time, end_time, amount, price, vid = None, None, None, None, None, None, None, None

    def __init__(self, order, vehicle):
        # self.id = order.id
        self.oid = order.id
        self.v_type = vehicle.type
        self.plate_num = vehicle.plateNum
        self.start_time = order.startTime
        self.end_time = order.endTime
        self.amount = order.amount
        self.price = vehicle.price
        self.vid = vehicle.id


class PaymentsItems:
    id, v_type, plate_num, amount, pay_time = None, None, None, None, None

    def __init__(self, payment, vehicle):
        self.id = payment.id
        self.v_type = vehicle.type
        self.plate_num = vehicle.plateNum
        self.amount = payment.amount
        self.pay_time = payment.payTime


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

    return render(request, "customers/vehicles_list.html", {"vehicles_available": vehicles_available})


# vehicle_details页面返回函数
def getVehicleDetails(request, vehicles_id):
    """
    根据前端返回的id，查找特定id的vehicle的信息
    返回这个车的所有信息
    path('/vehicle/vehicle_details/', ... )
    :param vid:
    :param request:
    :return:
    """
    details = models.Vehicles.objects.get(id=vehicles_id)
    return render(request, "customers/vehicles_detail.html", {"details": details})


def rent(request, vehicles_id):
    uid = globals.user_id
    user = models.Customers.objects.get(id=uid)

    if not user.eligible:
        error_message = "you can not rent more than one car at a time!"
        request.session['error_message'] = error_message
        request.session.set_expiry(1)
        return redirect('/rents/')
        # return render(request, "customers/vehicles_list.html", {'error_message': error_msg})
        # return HttpResponseRedirect(reverse('e_portal:rents'),
        #                             {"error_message": "you can not rent more than one car at a time!"})

    # 创建一个新的订单
    models.Order.objects.create(cid=uid, vid=vehicles_id)

    # update models
    models.Customers.objects.filter(id=uid).update(eligible=False)
    models.Vehicles.objects.filter(id=vehicles_id).update(status="using")

    msg = "Order created!"

    # return HttpResponseRedirect(reverse('e_portal:rents', args=(msg,)))
    return HttpResponseRedirect(reverse('e_portal:rents'))


def pay(request, order_id):
    order = models.Order.objects.filter(id=order_id)
    order.update(status="paid")

    # 新建Payments记录
    models.Payments.objects.create(amount=order[0].amount, cid=order[0].cid, vid=order[0].vid)
    # 更新用户totalSpending
    user = models.Customers.objects.filter(id=order[0].cid)
    user.update(totalSpending=user[0].totalSpending + order[0].amount)

    # redirect('customers/rents.html')
    return HttpResponseRedirect(reverse('e_portal:rents'))


def returnVehicle(request, order_id):
    uid = globals.user_id
    # 把endtime转为datetime形式
    end_time = timezone.now()
    # end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")

    # 拿到order和vehicle信息
    order = models.Order.objects.filter(id=order_id)
    vehicle = models.Vehicles.objects.filter(id=order[0].vid)

    # 计算费用并修改订单状态
    use_time = (end_time - order[0].startTime).seconds / 3600 + 1  # 使用时间
    amount = round(use_time * vehicle[0].price, 2)
    order.update(amount=amount, endTime=end_time)
    # unpaid_order = models.Order.objects.filter(cid=uid, status="unpaid")
    # 修改用户状态
    models.Customers.objects.filter(id=uid).update(eligible=True)
    # 修改车辆状态
    vehicle.update(batteryPercentage=vehicle[0].batteryPercentage - use_time * 10,
                   totalRentalHours=vehicle[0].totalRentalHours + use_time)
    if vehicle[0].batteryPercentage <= 20:
        vehicle.update(status="low_battery")
    else:
        vehicle.update(status="available")

    # redirect(request, '/rents/')
    return HttpResponseRedirect(reverse('e_portal:rents'))


def report(request, order_id):
    uid = globals.user_id
    # 把endtime转为datetime形式
    end_time = timezone.now()
    # end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")

    # 拿到order和vehicle信息
    order = models.Order.objects.filter(id=order_id)
    vehicle = models.Vehicles.objects.filter(id=order[0].vid)

    # 计算费用并修改订单状态
    use_time = (end_time - order[0].startTime).seconds / 3600 + 1  # 使用时间
    amount = round(use_time * vehicle[0].price, 2)
    order.update(amount=amount, endTime=end_time)
    # 修改用户状态
    models.Customers.objects.filter(id=uid).update(eligible=True)
    # 修改车辆状态为broken
    vehicle.update(status="broken")

    return HttpResponseRedirect(reverse('e_portal:rents'))


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

    cur_order = models.Order.objects.filter(endTime=None, cid=uid)
    unpaid_orders = models.Order.objects.filter(status="unpaid", cid=uid)
    unpaid_vehicles = list()
    for order in unpaid_orders:
        unpaid_vehicle = models.Vehicles.objects.get(id=order.vid)
        unpaid_vehicles.append(unpaid_vehicle)

    # oid, v_type, plate_num, start_time, end_time, amount, vid
    rents_items = list()
    for i in range(len(unpaid_orders)):
        if unpaid_orders[i].endTime is None:
            continue
        order = unpaid_orders[i]
        vehicle = unpaid_vehicles[i]
        item = RentsItems(order, vehicle)
        rents_items.append(item)

    if cur_order:
        cur_vid = cur_order[0].vid
        cur_vehicle = models.Vehicles.objects.get(id=cur_vid)
        cur_item = RentsItems(cur_order[0], cur_vehicle)

        return render(request, 'customers/rents.html', {"cur_item": cur_item, "rents_items": rents_items})
    else:
        return render(request, 'customers/rents.html', {"rents_items": rents_items})


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
    return render(request, 'pages/index.html', {"vehicle_all": vehicle_all})


def getPaymentHistory(request):
    payments = models.Payments.objects.all()
    paymentHistory = []
    for payment in payments:
        vehicle = models.Vehicles.objects.filter(id=payment.vid)
        paymentHistory.append(PaymentsItems(payment, vehicle[0]))
    return render(request, 'customers/payment_history.html', {"paymentHistory": paymentHistory})
