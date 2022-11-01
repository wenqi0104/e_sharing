from django.db import models
import django.utils.timezone as timezone


class Customers(models.Model):
    """
    用户表
    address: 地址
    nickName: 昵称，不能超过8个字符
    totalSpending: 该用户累计消费额
    balance: 用户当前余额
    email:
    password:
    createDate: 用户注册日期，需要在前端使用 {{value.date|date:'d-m-Y'}} 过滤
    updateDate: 对该记录最后更新的日期，作用未知. 操作同上
    eligible: 用户是否可以租车
    """
    address = models.CharField(max_length=64, default="")
    name = models.CharField(max_length=8)
    totalSpending = models.FloatField(default=0)
    # balance = models.FloatField(default=0)
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=16)
    createDate = models.DateTimeField(default=timezone.now)
    updateDate = models.DateTimeField(auto_now=True)
    eligible = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='resources/img/avatars', blank=True)


class Operators(models.Model):
    """
    操作人员表
    name:
    email:
    password:
    createDate: 同上
    updateDate: 同上
    """
    name = models.CharField(max_length=8)
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=16)
    createDate = models.DateTimeField(default=timezone.now)
    updateDate = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='resources/img/avatars', blank=True)


class Managers(models.Model):
    """
    操作人员表
    name:
    email:
    password:
    createDate: 同上
    updateDate: 同上
    """
    name = models.CharField(max_length=8)
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=16)
    createDate = models.DateTimeField(default=timezone.now)
    updateDate = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='resources/img/avatars', blank=True)


class Vehicles(models.Model):
    """
    type: 车辆类型
    cover: 封面  upload_to表示上传到哪个文件
    color:
    plateNum: 车牌号
    batteryPercentage:
    lastChargedTime:
    status: 车辆状态，有 broken/available/using/low_battery 四种
    totalRentalHours:
    locName: 车辆所在区域的名字
    latitude:
    longitude:
    price:
    """
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=8)
    cover = models.ImageField(upload_to='resources/img/covers', blank=True)
    color = models.CharField(max_length=8)
    # 车牌号从int修改char类型
    # plateNum = models.IntegerField(default=0)
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
    """
    管理员操作记录表
    operationType: 操作类型，存在 rent/return/charge/repair
    operateTime: 时间
    oid: 操作员的id
    vid: 车辆的id
    """
    operationType = models.CharField(max_length=8)
    operateTime = models.DateTimeField(timezone.now)
    oid = models.IntegerField(default=0)
    vid = models.IntegerField(default=0)


class Payments(models.Model):
    """
    支付表
    amount: 支付金额
    status: 支付是否成功  success/failed
    payTime: 支付时间
    cid: 用户id
    vid: 车辆id
    detail: 备注，主要用于支付失败显示失败原因
    """
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
    """
    车辆维修历史
    repairedLoc: 维修地点
    repairedTime: 维修时间
    oid:
    vid:
    """
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

