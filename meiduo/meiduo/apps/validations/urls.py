# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from django.urls import path
from validations.views import ImageCodeView

urlpatterns = [
    path('image_code/<image_code_id>', ImageCodeView.as_view(), name='image_code'),
]

