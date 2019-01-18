# -*- coding:utf-8 -*-
from areas import views

__author__ = 'xiaoguo'

from django.urls import path
from rest_framework.routers import DefaultRouter
from areas.views import AreasViewSet

urlpatterns = [
    # path('areas/', AreasViewSet.as_view(), name='areas'),
]

router = DefaultRouter()
router.register('areas', views.AreasViewSet, base_name='areas')
urlpatterns += router.urls


