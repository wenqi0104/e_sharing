"""
manager用户的所有接口
"""
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .. import models
# Create your views here.


def graphPage(request):
    """
    返回每种类型车的数量
    返回正在使用和可使用车的数量
    返回总盈利额
    返回每个月的盈利额
    :param request:
    :return:
    """
    # 返回每种类型车的数量
    type_car = ["bike", "scooter", "car"]
    type_list = []
    for i in range(len(type_car)):
        bike = models.Vehicles.objects.filter(type=type_car[i])
        amount = 0
        for x in bike:
            amount += 1
        type_list.append(amount)
    bike_amount = type_list[0]
    scooter_amount = type_list[1]
    car_amount = type_list[2]

    # 返回正在使用和可使用车的数量
    status_bike = ["using", "available"]
    status_list = []
    for i in range(len(status_bike)):
        status = models.Vehicles.objects.filter(status=status_bike[i])
        amount1 = 0
        for x in status:
            amount1 += 1
        status_list.append(amount1)
    using_amount = status_list[0]
    available_amount = status_list[1]

    # 返回总盈利额
    payment_successful = models.Payments.objects.filter(status="success")
    sum_payment = 0
    for i in payment_successful:
        amount2 = i.amount
        sum_payment += amount2

    # 返回每个月的盈利额
    month = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"]
    month_payment_list = []
    for i in range(len(month)):
        month_payment = models.Payments.objects.filter(payTime__year="2022", payTime__month=month[i], status="success")
        sum_month_payment = 0
        for x in month_payment:
            sum_month_payment += x.amount
        month_payment_list.append(sum_month_payment)
    return render(request, "managers/graph.html", {"type_list": type_list, "using_amount": using_amount,
                                "available_amount": available_amount, "sum_payment": sum_payment,
                                "month_payment": month_payment_list})
    

def tablePage(request):
    """
    返回车辆的所有信息
    :param request:
    :return:
    """
    vehicles_information = models.Vehicles.objects.all()
    return render(request, "managers/table.html", {"vehicles_information": vehicles_information})
