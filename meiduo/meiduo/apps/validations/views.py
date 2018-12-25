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

        # 保存短信验证码 发送记录
        redis_conn = get_redis_connection('verify_codes')
        # redis 管道

        pl = redis_conn.pipeline()

        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 管道通知redis执行命令
        pl.execute()

        # 发送短信
        try:
            ccp = CCP()
            expires = constants.SMS_CODE_REDIS_EXPIRES // 60
            result = ccp.send_template_sms(mobile, [sms_code, expires], constants.SMS_CODE_TEMP_ID)

        except Exception as e:
            logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
            return Response({'message': 'failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            if result == 0:
                logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
                try:
                    return Response({'message': 'OK'})
                except Exception as e:
                    print(e)
            else:
                logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)
                return Response({'message': 'failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


