# -*- coding:utf-8 -*-
from rest_framework import routers

from users import views

__author__ = 'xiaoguo'

from django.urls import path
from users.views import UserView, UsernameCountView, MobileCountView, UserDetailView, EmailView, VerifyEmailView
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('usernames/<username>/count/', UsernameCountView.as_view(), name='usernames'),
    path('mobiles/<int:mobile>/count/', MobileCountView.as_view(), name='mobiles'),
    path('authorizations/', obtain_jwt_token),                                  # 登录认证
    path('user/', UserDetailView.as_view(), name='user'),                       # 个人中心基本信息
    path('email/', EmailView.as_view(), name='email'),                          # 发送验证邮件
    path('emails/verification/', VerifyEmailView.as_view(), name='emails'),     # 邮箱验证
]

router = routers.DefaultRouter()
router.register('addresses', views.AddressViewSet, base_name='addresses')

urlpatterns += router.urls

