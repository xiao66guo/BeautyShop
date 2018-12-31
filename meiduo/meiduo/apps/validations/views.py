import random
import logging
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from meiduo.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from . import constants
from rest_framework.generics import GenericAPIView
from .serializer import ImageCodeCheckSerializer
from meiduo.utils.yuntongxun.sms import CCP
from celery_tasks.sms.tasks import send_sms_code

logger = logging.getLogger('django')
# Create your views here.

'''图片验证码视图'''
class ImageCodeView(APIView):
    def get(self, request, image_code_id):
        # 生成图片验证码
        text, image = captcha.generate_captcha()
        # 将图片验证码的真实值保存到Django_redis中
        redis_con = get_redis_connection('verify_codes')
        redis_con.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        print('图片验证码为：%s' % text)

        # 返回图片
        return HttpResponse(image, content_type='image/jpg')


'''短信验证码'''
class SMSCodeView(GenericAPIView):
    """
    发送短信验证码
    传入参数：
        mobile, image_code_id, text
    """
    serializer_class = ImageCodeCheckSerializer
    def get(self, request, mobile):
        # 校验参数（采用序列化器）
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        # print('短信验证码为：%d' % sms_code)

        # 保存短信验证码 发送记录
        redis_conn = get_redis_connection('verify_codes')
        # redis 管道
        pl = redis_conn.pipeline()
        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 管道通知redis执行命令
        pl.execute()

        print('短信验证码为：' + sms_code)

        # TODO:使用celery异步发送短信验证码
        expires = constants.IMAGE_CODE_REDIS_EXPIRES // 60
        send_sms_code.delay(mobile, sms_code, expires, constants.SMS_CODE_TEMP_ID)

        return Response({'message': 'OK'})

