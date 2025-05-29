# -*- coding: utf-8 -*-

"""
@author:lybbn
@date:2025-05-25
@Remark:管理后台登录视图
"""
import base64
from datetime import datetime, timedelta
from captcha.views import CaptchaStore, captcha_image
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from utils.apiview import CustomAPIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from mysystem.models import Users
from utils.jsonResponse import DetailResponse,ErrorResponse
from utils.request_util import save_login_log
from django_redis import get_redis_connection
from django.conf import settings
from config import IS_SINGLE_TOKEN

class CaptchaView(CustomAPIView):
    """
    获取图片验证码
    """
    authentication_classes = []

    def get(self, request):
        hashkey = CaptchaStore.generate_key()
        id = CaptchaStore.objects.filter(hashkey=hashkey).first().id
        imgage = captcha_image(request, hashkey)
        # 将图片转换为base64
        image_base = base64.b64encode(imgage.content)
        json_data = {"key": id, "image_base": "data:image/png;base64," + image_base.decode('utf-8')}
        return DetailResponse(data=json_data)

class LoginSerializer(TokenObtainPairSerializer):
    """
    登录的序列化器:
    重写djangorestframework-simplejwt的序列化器
    """
    captcha = serializers.CharField(max_length=6)

    @classmethod
    def get_token(cls, user):
        refresh = super(LoginSerializer,cls).get_token(user)
        data = {}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id"]

    default_error_messages = {
        'no_active_account': _('该账号已被禁用,请联系管理员')
    }


class LoginView(CustomAPIView):
    """
    登录接口
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer  # 显式声明序列化器

    #删除验证码
    def delete_expire_captcha(self):
        five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
        CaptchaStore.objects.filter(expiration__lte = five_minute_ago).delete()

    def post(self, request):
        username = request.data.get('username',None)
        password = request.data.get('password',None)
        captchaKey = request.data.get('captchaKey',None)
        captcha = request.data.get('captcha',None)

        image_code = CaptchaStore.objects.filter(id=captchaKey).first()
        five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
        if image_code and five_minute_ago > image_code.expiration:
            self.delete_expire_captcha()
            msg="验证码过期"
            save_login_log(request=request,status=False,msg=msg)
            return ErrorResponse(msg=msg)
        else:
            if image_code and (image_code.response == captcha or image_code.challenge == captcha):
                image_code and image_code.delete()
            else:
                self.delete_expire_captcha()
                msg="图片验证码错误"
                save_login_log(request=request,status=False,msg=msg)
                return ErrorResponse(msg=msg)
            
        user = Users.objects.filter(username=username).first()

        if not user:
            return ErrorResponse(msg="账号/密码错误")

        if user and not user.is_staff:#判断是否允许登录后台
            msg="您没有权限登录后台"
            save_login_log(request=request,status=False,msg=msg)
            return ErrorResponse(msg=msg)
        
        if user and not user.is_active:
            msg="该账号已被禁用"
            save_login_log(request=request,status=False,msg=msg)
            return ErrorResponse(msg=msg)

        if user and user.check_password(password):  # check_password() 对明文进行加密,并验证
            data = LoginSerializer.get_token(user)
            msg="登录成功"
            save_login_log(request=request,status=True,msg=msg)
            # 缓存用户的jwt token
            if IS_SINGLE_TOKEN:
                redis_conn = get_redis_connection("singletoken")
                k = "lybbn-single-token{}".format(user.id)
                TOKEN_EXPIRE_CONFIG = getattr(settings, 'SIMPLE_JWT', None)
                if TOKEN_EXPIRE_CONFIG:
                    TOKEN_EXPIRE = TOKEN_EXPIRE_CONFIG['ACCESS_TOKEN_LIFETIME']
                    redis_conn.set(k, data['access'], TOKEN_EXPIRE)
            return DetailResponse(data=data,msg=msg)
        else:
            msg="账号/密码错误"
            save_login_log(request=request,status=False,msg=msg)
            return ErrorResponse(msg=msg)