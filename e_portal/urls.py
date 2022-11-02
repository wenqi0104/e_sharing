from django.urls import path, include
from .views import log, customer, manager, operator
from django.urls import path

app_name = 'e_portal'
urlpatterns = [
    # log
    # path('', log.index, name='index'),
    path('', log.login, name='login'),
    path("main/", log.index, name='index'),
    path("register/", log.register, name='register'),
    path("pwd_reset/", log.pwd_reset, name='pwd_reset'),
    path("error404/", log.Error404, name='error404'),

    # customer
    path("vehicles/", customer.getAvailableVehicles, name='vehicles_list'),
    # 进入details页面执行的
    path("vehicles/<int:vehicles_id>/", customer.getVehicleDetails, name='vehicles_detail'),

    # 在details页面执行，rent a car
    path("rent/<int:vehicles_id>/", customer.rent, name='rent'),

    # customer pay
    path("pay/<int:order_id>/", customer.pay, name='payment'),

    # customer report a broken car
    path("report/<int:order_id>/", customer.report, name='report'),

    # return a car
    path("return/<int:order_id>/", customer.returnVehicle, name='returnVehicle'),
    # rental info page
    path("rents/", customer.rents, name='rents'),
    # payment history
    path("history/",customer.getPaymentHistory, name='paymentHistory'),

    # operator
    path("operators/vehicles_using/", operator.getUsingVehicles, name='vehicles_using'),
    path("operators/vehicles_available/", operator.getUnUsingVehicles, name='vehicles_available'),
    path("operators/vehicles_deal/", operator.getDealVehicles, name='vehicles_deal'),
    path("move/", operator.moveVehicles),
    path("charge/", operator.chargeVehicles),
    path("repair/", operator.repairVehicles),
    # debugging
    path("vehicles_using/", operator.getUsingVehicles),
    path("vehicles_unusing/", operator.getUnUsingVehicles),
    path("vehicles_move/", operator.moveVehicles),
    path("vehicles_deal/", operator.getDealVehicles),

    # managers
    path("managers/graph", manager.graphPage),
    path("managers/table", manager.graphPage),
]
