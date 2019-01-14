from django.shortcuts import render

#TODO:第三方登录
# 获取QQ登录的URL
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from oauth.exceptions import OAuthQQAPIError
from oauth.models import OAuthQQUser
from oauth.serializer import OAuthQQUserSerializer
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


class QQAuthUserView(CreateAPIView):

    serializer_class = OAuthQQUserSerializer

    def get(self, request):
        # 获取code
        code = request.query_params.get('code')

        if not code:
            return Response({'message': 'no have code'}, status=status.HTTP_400_BAD_REQUEST)

        # 根据获取的code来获取access_token
        oauth_qq = OAuthQQ()
        try:
            access_token = oauth_qq.get_access_token(code)
            # 根据access_token获取openid
            openid = oauth_qq.get_openid(access_token)
            # print(access_token, openid)
        except OAuthQQAPIError:
            return Response({'message': '访问QQ接口异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 根据获取的openID查询数据库OAuthQQUser 判断数据是否存在
        try:
            oauth_qq_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 如果数据不存在，处理openID并进行返回
            access_token = oauth_qq.generate_bind_user_access_token(openid)
            return Response({'access_token': access_token})

        else:
            # 如果数据存在，表示用户已经绑定过身份，签发 jwt token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            user = oauth_qq_user.user
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            return Response({
                'username': user.username,
                'user_id': user.id,
                'token': token,
            })

    # def post(self, request):

