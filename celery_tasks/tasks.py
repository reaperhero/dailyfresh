from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
app = Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379/0')

# celery 单独启动需要做以下初始化
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
# django.setup()

# 定义任务函数
@app.task(name='send_register_active_email')
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""
    subject = '天天生鲜欢迎信息'
    message = ''
    html_message = '<h1>%s, 欢迎你成为天天生鲜注册会员</h1>请点击下面连接激活你的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
    username, token, token)
    sender = settings.EMAIL_FROM
    reveiver = [to_email]
    send_mail(subject=subject, message=message, from_email=sender, recipient_list=reveiver, html_message=html_message)