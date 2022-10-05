from django.shortcuts import render


# Create your views here
# 第一步，create app，  使用： python manage.py startapp app的名字， 然后在根app的setting.py中手动注册app
# 第二步，views中注册html页面，用render（）方法，
# 第三步，urls中注册路由
# 第四步，写html页面
def index(request):
    # 这里的pages/index.html就是具体的文件
    return render(request, 'pages/index.html')
