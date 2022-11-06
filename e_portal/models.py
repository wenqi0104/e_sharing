from django.db import models
import django.utils.timezone as timezone


class Customers(models.Model):
    name = models.CharField(max_length=8)
    totalSpending = models.FloatField(default=0)
    # balance = models.FloatField(default=0)    # deleted
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=16)
    createDate = models.DateTimeField(default=timezone.now)
    eligible = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='resources/img/avatars', default='resources/img/avatars/new_user.jpg')


class Operators(models.Model):
    name = models.CharField(max_length=8)
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=16)
    createDate = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to='resources/img/avatars', blank=True)


class Managers(models.Model):
    name = models.CharField(max_length=8)
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=16)
    createDate = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to='resources/img/avatars', blank=True)


class Vehicles(models.Model):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=8)
    cover = models.ImageField(upload_to='resources/img/covers', blank=True)
    color = models.CharField(max_length=8)
    plateNum = models.CharField(max_length=7)
    batteryPercentage = models.IntegerField(default=100)
    lastChargedTime = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=32, default='available')
    totalRentalHours = models.FloatField(default=0)
    locName = models.CharField(max_length=128)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    price = models.FloatField(default=0)
    description = models.TextField(blank=True, null=True)


class OperationsHistory(models.Model):
    operationType = models.CharField(max_length=8)
    operateTime = models.DateTimeField(timezone.now)
    oid = models.IntegerField(default=0)
    vid = models.IntegerField(default=0)


class Payments(models.Model):
    amount = models.FloatField(blank=False)
    status = models.CharField(max_length=8, default='success')
    payTime = models.DateTimeField(default=timezone.now)
    cid = models.IntegerField()
    vid = models.IntegerField()
    detail = models.CharField(max_length=128, default="")


# class TopUpHistory(models.Model):
#     """
#     用户充值记录表
#     amount: 充值金额
#     status:
#     topTime:
#     cid:
#     detail:
#     """
#     amount = models.IntegerField(blank=False)
#     status = models.CharField(max_length=8)
#     topTime = models.DateTimeField(timezone.now)
#     cid = models.ForeignKey('Customers', on_delete=models.CASCADE)
#     detail = models.CharField(max_length=128)


class RepairHistory(models.Model):
    repairedLoc = models.CharField(max_length=16)
    repairedTime = models.DateTimeField(timezone.now)
    oid = models.IntegerField(default=0)
    vid = models.IntegerField(default=0)


class Order(models.Model):
    amount = models.FloatField(default=0.0)
    status = models.CharField(default='unpaid', max_length=16)
    startTime = models.DateTimeField(default=timezone.now)
    endTime = models.DateTimeField(null=True, blank=True)
    cid = models.IntegerField(default=0)
    vid = models.IntegerField(default=0)

