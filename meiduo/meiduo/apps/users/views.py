from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from users import serializers

class UserView(CreateAPIView):
    serializer_class = serializers.CreateUserSerializer
