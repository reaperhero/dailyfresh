import re

from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views import View

from django.conf import settings
from user.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from celery_tasks.tasks import send_register_active_email


# Create your views here.


# /user/register
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        # 注册处理
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 数据是否为空
        if not all([username, password, email]):
            print("as")
            return render(request, 'register.html', {
                'errmsg': '数据不完整'
            })

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            print("ad")
            return render(request, 'register.html', {
                'errmsg': '邮箱格式不正确'
            })

        if allow != 'on':
            print("as")
            return render(request, 'register.html', {
                'errmsg': '请同意协议'
            })

        try:
            user = User.objects.get(username=username)
        except user.DoesNotExist:
            # 用户已存在
            user = None
        if user:
            return render(request, 'register.html', {
                'errmsg': '用户名已存在'
            })
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        return redirect(reverse('goods:index'))


# 类视图的使用
# /user/register
class RegisterView(View):
    """注册"""

    def get(self, request):
        """显示注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """进行注册处理"""
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {
                'errmsg': '邮箱格式不正确'
            })

        if allow != 'on':
            return render(request, 'register.html', {
                'errmsg': '请同意协议'
            })

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'register.html', {'errmsg': '用户名已存在'})
        # 进行业务处理: 进行用户注册
        user = User.objects.create_user(username, email, password)
        # 激活字段，默认为没有激活
        user.is_active = 0
        user.save()
        # 发送激活邮件，包含激活连接： http：//127.0.0.1：8000/user/active/用户id
        # 激活连接中需要包含用户的身份信息，并且要把身份信息进行加密处理
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)
        token = token.decode()

        send_register_active_email.delay(email,username,token)
        # 跳转首页
        return redirect(reverse('goods:index'))


class ActiveView(View):
    # 用户激活
    def get(self, request, token):
        # 进行解密
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活链接过期
            return HttpResponse('激活链接已经过期')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        """登陆校验"""
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        if not all([username,password]):
            return render(request,'login.html',{
                'errmsg':'数据不完整'
            })
            # 业务处理： 登陆校验
            # 自动密码加密对比
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名已激活
            if user.is_active:
                # 用户已激活
                # 记录用户的登陆状态
                login(request, user)
                return redirect((reverse('goods:index')))
            else:
                # 用户未激活
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})
