# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from django.urls import path
from users.views import UserView, UsernameCountView, MobileCountView
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('usernames/<username>/count/', UsernameCountView.as_view(), name='usernames'),
    path('mobiles/<int:mobile>/count/', MobileCountView.as_view(), name='mobiles'),
    path('authorizations/', obtain_jwt_token),         # 登录认证

]

