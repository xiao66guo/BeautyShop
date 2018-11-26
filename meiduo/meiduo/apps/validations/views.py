from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from meiduo.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from . import constants

# Create your views here.

'''图片验证码视图'''
class ImageCodeView(APIView):
    def get(self, request, image_code_id):
        # 生成图片验证码
        text, image = captcha.generate_captcha()
        # 将图片验证码的真实值保存到Django_redis中
        redis_con = get_redis_connection('verify_codes')
        redis_con.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        # 返回图片
        return HttpResponse(image, content_type='image/jpg')