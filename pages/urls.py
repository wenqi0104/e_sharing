# _*_ coding : utf-8 _*_
# @Time : 2022/9/25 16:45
# @Author : Wenqi Zhang
# @File : urls
# @Project : djangoProjects


from django.urls import path
from . import views
from e_portal import views as pviews

urlpatterns = [
    # 这里的index是定义在views里的index方法名
    # 填空就是默认进入的页面
    path('', pviews.test),
]


