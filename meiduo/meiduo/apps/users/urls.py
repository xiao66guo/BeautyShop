# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from django.urls import path
from users.views import UserView



urlpatterns = [
    path('users/', UserView.as_view(), name='users'),

]

