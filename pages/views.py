from django.shortcuts import render
from django.views import View


# Create your views here
# 第一步，create app，  使用： python manage.py startapp app的名字， 然后在根app的setting.py中手动注册app
# 第二步，views中注册html页面，用render（）方法，
# 第三步，urls中注册路由
# 第四步，写html页面
def index(request):
    # 这里的pages/index.html就是具体的文件
    return render(request, 'pages/index.html')


class Login(View):
    # 默认渲染页面的方式，没有任何操作，也没有传入任何值
    def get(self, request):
        return render(request, 'pages/login.html')


class Register(View):
    # 默认渲染页面的方式，没有任何操作，也没有传入任何值
    def get(self, request):
        return render(request, 'pages/register.html')


class PwdRest(View):
    # 默认渲染页面的方式，没有任何操作，也没有传入任何值
    def get(self, request):
        return render(request, 'pages/pwd_reset.html')

class Error404(View):
    # 默认渲染页面的方式，没有任何操作，也没有传入任何值
    def get(self, request):
        return render(request, 'pages/404.html')