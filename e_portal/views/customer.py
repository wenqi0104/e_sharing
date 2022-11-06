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
    Return all available vehicles
    :param request:
    :return:
    """
    vehicles_available = models.Vehicles.objects.filter(status="available")

    # make sure the message only shows once.
    if request.session.get('error_message') is not None:
        del request.session['error_message']

    if request.session.get('rent_success') is not None:
        del request.session['rent_success']

    if request.session.get('pay_success') is not None:
        del request.session['pay_success']

    return render(request, "customers/vehicles_list.html", {"vehicles_available": vehicles_available})


def getVehicleDetails(request, vehicles_id):
    """
    Return the specific vehicle details
    :param vehicles_id: the ID of the vehicle
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
        return HttpResponseRedirect(reverse('e_portal:rents'))

    # create a new order
    models.Order.objects.create(cid=uid, vid=vehicles_id)

    # update models
    models.Customers.objects.filter(id=uid).update(eligible=False)
    models.Vehicles.objects.filter(id=vehicles_id).update(status="using")

    rent_success = "Rent successfully!"
    request.session['rent_success'] = rent_success

    return HttpResponseRedirect(reverse('e_portal:rents'))


def pay(request, order_id):
    order = models.Order.objects.filter(id=order_id)
    order.update(status="paid")

    # create a new Payment
    models.Payments.objects.create(amount=order[0].amount, cid=order[0].cid, vid=order[0].vid)
    # Cal totalSpending
    user = models.Customers.objects.filter(id=order[0].cid)
    user.update(totalSpending=user[0].totalSpending + order[0].amount)
    pay_success = 'Pay successfully!'
    request.session['pay_success'] = pay_success

    return HttpResponseRedirect(reverse('e_portal:rents'))


def returnVehicle(request, order_id):
    uid = globals.user_id
    end_time = timezone.now()

    order = models.Order.objects.filter(id=order_id)
    vehicle = models.Vehicles.objects.filter(id=order[0].vid)

    # The minimum use_time is 0.5 hour, any use_time smaller than 0.5 hour will be calculated as 0.5 hour.
    use_time = round((end_time - order[0].startTime).seconds / 3600, 2) + 0.5
    amount = round(use_time * vehicle[0].price, 2)
    order.update(amount=amount, endTime=end_time)

    models.Customers.objects.filter(id=uid).update(eligible=True)
    # update the status of this vehicle.
    temp_battery = round(vehicle[0].batteryPercentage - use_time * 10, 2)
    new_battery = 0 if temp_battery < 0 else temp_battery
    vehicle.update(batteryPercentage=new_battery,
                   totalRentalHours=vehicle[0].totalRentalHours + use_time)
    if vehicle[0].batteryPercentage <= 20:
        vehicle.update(status="low_battery")
    else:
        vehicle.update(status="available")

    return HttpResponseRedirect(reverse('e_portal:rents'))


def report(request, order_id):
    uid = globals.user_id
    end_time = timezone.now()

    order = models.Order.objects.filter(id=order_id)
    vehicle = models.Vehicles.objects.filter(id=order[0].vid)

    # Cal amount and update related status in the database
    # The minimum use_time is 0.5 hour, any use_time smaller than 0.5 hour will be calculated as 0.5 hour.
    use_time = round((end_time - order[0].startTime).seconds / 3600, 2) + 0.5
    amount = round(use_time * vehicle[0].price, 2)
    order.update(amount=amount, endTime=end_time)
    # eligible = true, so the user can rent another vehicle.
    models.Customers.objects.filter(id=uid).update(eligible=True)
    # update the status of this vehicle being broken
    temp_battery = round(vehicle[0].batteryPercentage - use_time * 10, 2)
    new_battery = 0 if temp_battery < 0 else temp_battery
    vehicle.update(status="broken", batteryPercentage=new_battery,
                   totalRentalHours=vehicle[0].totalRentalHours + use_time)

    return HttpResponseRedirect(reverse('e_portal:rents'))


def rents(request):
    uid = globals.user_id

    cur_order = models.Order.objects.filter(endTime=None, cid=uid)
    unpaid_orders = models.Order.objects.filter(status="unpaid", cid=uid)
    unpaid_vehicles = list()
    for order in unpaid_orders:
        unpaid_vehicle = models.Vehicles.objects.get(id=order.vid)
        unpaid_vehicles.append(unpaid_vehicle)

    # organize info into one RentsItems object, easy for font-end to iterate
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


def showMap(request):
    """
    Return all vehicles that will be shown on the map
    :param request:
    :return:
    """
    vehicle_all = models.Vehicles.objects.all()
    return render(request, 'pages/index.html', {"vehicle_all": vehicle_all})


def getPaymentHistory(request):
    """
    Return the payment history of current customer.
    """
    uid = globals.user_id
    payments = models.Payments.objects.filter(cid=uid)
    payment_history = []
    for payment in payments:
        vehicle = models.Vehicles.objects.filter(id=payment.vid)
        payment_history.append(PaymentsItems(payment, vehicle[0]))

    # make sure the message will show only once!
    if request.session.get('error_message') is not None:
        del request.session['error_message']

    if request.session.get('rent_success') is not None:
        del request.session['rent_success']

    if request.session.get('pay_success') is not None:
        del request.session['pay_success']

    return render(request, 'customers/payment_history.html', {"paymentHistory": payment_history})
