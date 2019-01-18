from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from areas import serializer
from areas.models import Area


class AreasViewSet(CacheResponseMixin,ReadOnlyModelViewSet):
    pagination_class = None

    def get_queryset(self):
        if self.action == 'list':
            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()


    def get_serializer_class(self):
        if self.action == 'list':
            return serializer.AreaSerializer
        else:
            return serializer.SubAreaSerializer
    pass


