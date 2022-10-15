# _*_ coding : utf-8 _*_
# @Time : 2022/9/25 16:45
# @Author : Wenqi Zhang
# @File : urls
# @Project : djangoProjects


from django.urls import path
from . import views
from .views import Login,Register

urlpatterns = [
    # 这里的index是定义在views里的index方法名
    # 填空就是默认进入的页面
    path('', views.index, name='index'),
    path("login/", Login.as_view(), name='login'),
    path("register/", Register.as_view(), name='register')

]


