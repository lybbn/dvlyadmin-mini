"""
日志 django中间件
"""
import json,re

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from mysystem.models import OperationLog
from utils.request_util import get_request_user, get_request_ip, get_request_data, get_request_path, get_os,get_browser, get_verbose_name

from django.http import HttpResponseForbidden,HttpResponse
from config import ALLOW_FRONTEND,FRONTEND_API_LIST,IS_SINGLE_TOKEN
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication,JWTTokenUserAuthentication
from rest_framework.views import APIView
from utils.jsonResponse import SuccessResponse,ErrorResponse
from utils.common import get_parameter_dic
from django_redis import get_redis_connection

from django.contrib.auth.models import AnonymousUser, User

IS_ALLOW_FRONTEND = ALLOW_FRONTEND

class ApiLoggingMiddleware(MiddlewareMixin):
    """
    用于记录API访问日志中间件
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.enable = getattr(settings, 'API_LOG_ENABLE', None) or False
        self.methods = getattr(settings, 'API_LOG_METHODS', None) or set()
        self.request_modular = ""

    @classmethod
    def __handle_request(cls, request):
        request.request_ip = get_request_ip(request)
        request.request_data = get_request_data(request)
        request.request_path = get_request_path(request)

    def __handle_response(self, request, response):
        # request_data,request_ip由PermissionInterfaceMiddleware中间件中添加的属性
        body = getattr(request, 'request_data', {})
        # 请求含有password则用*替换掉(暂时先用于所有接口的password请求参数)
        if isinstance(body, dict) and body.get('password', ''):
            body['password'] = '*' * len(body['password'])
        if isinstance(body, dict) and body.get('oldPassword', '') and body.get('newPassword', '') and body.get('newPassword2', ''):
            body['oldPassword'] = '*' * len(body['oldPassword'])
            body['newPassword'] = '*' * len(body['newPassword'])
            body['newPassword2'] = '*' * len(body['newPassword2'])
        if not hasattr(response, 'data') or not isinstance(response.data, dict):
            response.data = {}
        try:
            if not response.data and response.content:
                content = json.loads(response.content.decode())
                response.data = content if isinstance(content, dict) else {}
        except Exception:
            return
        user = get_request_user(request)
        request_ip = getattr(request, 'request_ip', 'unknown')
        info = {
            'req_ip': request_ip,
            'creator': user if not isinstance(user, AnonymousUser) else None,
            'dept_belong': getattr(request.user, 'dept_id', None),
            'req_method': request.method,
            'req_path': request.request_path,
            'req_body': body,
            'resp_code': response.data.get('code'),
            'req_os': get_os(request),
            'req_browser': get_browser(request),
            'req_msg': request.session.get('request_msg'),
            'status': True if response.data.get('code') in [2000, ] else False,
            'json_result': {"code": response.data.get('code'),"data":response.data.get('data'), "msg": response.data.get('msg')},
        }
        temp_request_modular = ""
        if not self.request_modular and settings.API_MODEL_MAP.get(request.request_path, None):
            temp_request_modular = settings.API_MODEL_MAP[request.request_path]
        else:
            temp_request_modular = self.request_modular

        operation_log = OperationLog.objects.create(req_modular=temp_request_modular,req_ip=info['req_ip'],ip_area="",creator=info['creator'],dept_belong=info['dept_belong'],req_method=info['req_method'],req_path=info['req_path'],req_body=info['req_body'],resp_code=info['resp_code'],req_os=info['req_os'],req_browser=info['req_browser'],req_msg=info['req_msg'],status=info['status'],json_result=info['json_result'])

        self.request_modular = ""

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(view_func, 'cls') and hasattr(view_func.cls, 'queryset'):
            if self.enable:
                if self.methods == 'ALL' or request.method in self.methods:
                    self.request_modular = get_verbose_name(view_func.cls.queryset)

        return None
    def process_request(self, request):
        self.__handle_request(request)

        if IS_SINGLE_TOKEN:#保证设备登录的唯一性
            if request.request_path[0:9] not in FRONTEND_API_LIST:
                jwt_token = request.META.get('HTTP_AUTHORIZATION', None)
                if jwt_token and 'JWT' in jwt_token and jwt_token.split('JWT ')[1]!='null':
                    errordata = {'msg': '身份认证已经过期，请重新登入', 'code': 4001, 'data': ''}
                    try:
                        user,token = JWTTokenUserAuthentication().authenticate(request)
                        redis_conn = get_redis_connection("singletoken")
                        k = "lybbn-single-token{}".format(user.id)
                        cache_token = redis_conn.get(k)
                        if cache_token:
                            if not str(token) == str(cache_token):
                                return HttpResponse(json.dumps(errordata), content_type='application/json',status=200,charset='utf-8')
                        else:
                            return HttpResponse(json.dumps(errordata), content_type='application/json',status=200,charset='utf-8')
                    except Exception as e:
                        print(e)
                        return HttpResponse(json.dumps(errordata), content_type='application/json',status=200,charset='utf-8')

    def process_response(self, request, response):
        """
        主要请求处理完之后记录
        :param request:
        :param response:
        :return:
        """
        if self.enable:
            if self.methods == 'ALL' or request.method in self.methods:
                self.__handle_response(request, response)

        # 过滤前端接口关闭情况
        if not IS_ALLOW_FRONTEND:
            if FRONTEND_API_LIST:
                for i in FRONTEND_API_LIST:
                    if i in request.request_path:
                        return HttpResponseForbidden('<h1>Access Forbidden 301</h1>')

        return response

class OperateAllowFrontendView(APIView):
    """
    超级管理员动态启用/禁用/获取 禁止前端接口访问
    get:
    获取当前是否禁止前端访问的值
    【参数】无
    post:
    设置当前是否禁止前端访问
    【参数】is_allow = 1 允许访问  0 禁止访问
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
        获取当前是否禁止前端访问的值
        """
        data = {
            'is_allow':IS_ALLOW_FRONTEND
        }
        return SuccessResponse(data=data,msg='success')

    def post(self,request):
        """
        设置当前是否禁止前端访问
        """
        user = request.user
        if user.is_superuser:
            global IS_ALLOW_FRONTEND
            is_allow = int(get_parameter_dic(request)['is_allow'])

            if is_allow:
                IS_ALLOW_FRONTEND = True
            else:
                IS_ALLOW_FRONTEND = False
            data = {
                'is_allow': IS_ALLOW_FRONTEND
            }
            return SuccessResponse(data=data,msg='设置成功')
        else:
            return ErrorResponse(msg="您没有权限操作")