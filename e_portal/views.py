from e_portal import models
from django.shortcuts import render, HttpResponse


# 数据库操作部分
def test(request):
    # models.Customers.objects.create(address="UofG", nickName="Cold glows", totalSpending=12.3,
    #                                 email="UofGtime@gmail.com", password="123321.")

    # models.Operators.objects.create(name='wsw', email='go@gmail.com', password='123321.')
    #
    # models.Vehicles.objects.create(type='单车', cover='C:\\Users\\Shiwei\\Desktop\\1.png', color='red',
    #                                status='available', locName='UofG')

    return HttpResponse("数据库测试")
