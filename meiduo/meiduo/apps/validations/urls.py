# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from django.urls import path
from . import views

urlpatterns = [
    path('imageCodeView/<image_code_id>', views.ImageCodeView.as_view(), name='imageCodeView'),
]

