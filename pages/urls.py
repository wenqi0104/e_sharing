# _*_ coding : utf-8 _*_
# @Time : 2022/9/25 16:45
# @Author : Wenqi Zhang
# @File : urls
# @Project : djangoProjects


from django.urls import path
from . import views
from .views import Login, Register, PwdRest, Error404

app_name = 'pages'
urlpatterns = [
    # 这里的index是定义在views里的index方法名
    # 填空就是默认进入的页面
    path('', views.index, name='index'),
    path("login/", Login.as_view(), name='login'),
    path("register/", Register.as_view(), name='register'),
    path("pwd_reset/", PwdRest.as_view(), name='pwd_reset'),
    path("error404/", Error404.as_view(), name='error404'),

]

