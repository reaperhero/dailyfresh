import re

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from user.models import User


# Create your views here.


# /user/register


def register(request):
    return render(request, 'register.html')


def register_handle(request):
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
