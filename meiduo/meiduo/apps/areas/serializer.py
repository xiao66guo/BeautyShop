# -*- coding:utf-8 -*-
from rest_framework import serializers

from areas.models import Area

__author__ = 'xiaoguo'


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name')


class SubAreaSerializer(serializers.ModelSerializer):
    subs = AreaSerializer(many=True, read_only=True)
    class Meta:
        model = Area
        fields = ('id', 'name', 'subs')


