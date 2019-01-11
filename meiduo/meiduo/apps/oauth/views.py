from django.shortcuts import render

#TODO:第三方登录
# 获取QQ登录的URL
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth.utils import OAuthQQ


class QQAuthURLView(APIView):
    def get(self, request):
        # 获取next参数
        next = request.query_params.get('next')

        # 拼接QQ的登录网址
        oauth_qq = OAuthQQ(state=next)
        login_url = oauth_qq.get_login_url()

        # 返回
        return Response({'login_url': login_url})


class QQAuthUserView(APIView):

    def get(self, request):
        # 获取code
        code = request.query_params.get('code')

        if not code:
            return Response({'message': 'no have code'}, status=status.HTTP_400_BAD_REQUEST)

        # 根据获取的code来获取access_token
        oauth_qq = OAuthQQ()
        access_token = oauth_qq.get_access_token()
    pass
