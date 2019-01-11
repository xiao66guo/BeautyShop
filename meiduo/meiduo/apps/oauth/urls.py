# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from django.urls import path
from oauth.views import QQAuthURLView


urlpatterns = [
    path('qq/authorization/', QQAuthURLView.as_view(), name='qq'),

]

