# -*- coding:utf-8 -*-
from django.contrib.auth.backends import ModelBackend
import re
from .models import User
__author__ = 'xiaoguo'

def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


# 根据账号获取用户对象
def get_user_by_account(account):
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user



# TODO:自定义用户名或手机号认证
class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 获取用户对象
        user = get_user_by_account(username)

        if user is not None and user.check_password(password):
            return user
