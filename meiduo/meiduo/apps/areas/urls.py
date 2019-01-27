# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from django.urls import path
from rest_framework.routers import DefaultRouter
from areas import views

urlpatterns = []

router = DefaultRouter()
router.register('areas', views.AreasViewSet, base_name='areas')
urlpatterns += router.urls


