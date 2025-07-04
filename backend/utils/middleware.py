"""
@Author：lybbn
@QQ：1042594286
@EditDate：2025-07-04
@Version：1.0
日志 django中间件
"""
import json
import re
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from mysystem.models import OperationLog
from utils.request_util import (
    get_request_user, 
    get_request_ip, 
    get_request_data, 
    get_request_path, 
    get_os,
    get_browser, 
    get_verbose_name
)
from django.http import HttpResponseForbidden, HttpResponse
from config import ALLOW_FRONTEND, FRONTEND_API_LIST, IS_SINGLE_TOKEN
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTTokenUserAuthentication
from rest_framework.views import APIView
from utils.jsonResponse import SuccessResponse, ErrorResponse
from utils.common import get_parameter_dic
from django_redis import get_redis_connection
from django.contrib.auth.models import AnonymousUser

class ApiLoggingMiddleware(MiddlewareMixin):
    """
    用于记录API访问日志中间件
    优化点：
    1. 使用类变量存储全局配置
    2. 优化日志记录逻辑
    3. 添加类型提示
    4. 优化异常处理
    5. 代码结构更清晰
    """

    # 类变量存储配置
    enable = getattr(settings, 'API_LOG_ENABLE', False)
    methods = getattr(settings, 'API_LOG_METHODS', set())
    IS_ALLOW_FRONTEND = ALLOW_FRONTEND

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.request_modular = ""

    def _handle_request(self, request):
        """处理请求信息"""
        request.request_ip = get_request_ip(request)
        request.request_data = get_request_data(request)
        request.request_path = get_request_path(request)

    def _mask_sensitive_data(self, data: dict) -> dict:
        """掩码敏感数据"""
        sensitive_fields = ['password', 'currentPassword', 'newPassword', 'confirmPassword']
        for field in sensitive_fields:
            if field in data and data[field]:
                data[field] = '*' * len(data[field])
        return data

    def _get_response_data(self, response):
        """获取响应数据"""
        if not hasattr(response, 'data') or not isinstance(response.data, dict):
            response.data = {}
        
        if not response.data and response.content:
            try:
                content = json.loads(response.content.decode())
                response.data = content if isinstance(content, dict) else {}
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
        return response.data

    def _create_operation_log(self, request, response):
        """创建操作日志"""
        body = self._mask_sensitive_data(getattr(request, 'request_data', {}))
        response_data = self._get_response_data(response)
        
        user = get_request_user(request)
        request_ip = getattr(request, 'request_ip', 'unknown')
        tmpuser = user if not isinstance(user, AnonymousUser) else None
        log_info = {
            'req_ip': request_ip,
            'creator': tmpuser,
            'creator_name':tmpuser.username if tmpuser else "",
            'dept_belong': getattr(request.user, 'dept_id', None),
            'req_method': request.method,
            'req_path': request.request_path,
            'req_body': body,
            'resp_code': response_data.get('code'),
            'req_os': get_os(request),
            'req_browser': get_browser(request),
            'req_msg': request.session.get('request_msg'),
            'status': response_data.get('code') in [2000,],
            'json_result': {
                "code": response_data.get('code'),
                "data": response_data.get('data'),
                "msg": response_data.get('msg')
            },
        }

        # 获取模块名称
        temp_request_modular = (
            settings.API_MODEL_MAP.get(request.request_path, "")
            if not self.request_modular
            else self.request_modular
        )

        OperationLog.objects.create(
            req_modular=temp_request_modular,
            ip_area="",  # 可以考虑添加IP地区解析功能
            **log_info
        )

    def process_view(self, request, view_func, view_args, view_kwargs):
        """处理视图前设置模块名称"""
        if self.enable and hasattr(view_func, 'cls') and hasattr(view_func.cls, 'queryset'):
            if self.methods == 'ALL' or request.method in self.methods:
                self.request_modular = get_verbose_name(view_func.cls.queryset)
        return None

    def process_request(self, request):
        """处理请求"""
        self._handle_request(request)

        # 单点登录验证
        if IS_SINGLE_TOKEN and request.request_path[0:9] not in FRONTEND_API_LIST:
            jwt_token = request.META.get('HTTP_AUTHORIZATION', '')
            if jwt_token and 'JWT' in jwt_token and jwt_token.split('JWT ')[1] != 'null':
                error_data = {'msg': '身份认证已经过期，请重新登入', 'code': 4001, 'data': ''}
                try:
                    user, token = JWTTokenUserAuthentication().authenticate(request)
                    redis_conn = get_redis_connection("singletoken")
                    cache_token = redis_conn.get(f"lybbn-single-token{user.id}")
                    
                    if not cache_token or str(token) != str(cache_token):
                        return HttpResponse(
                            json.dumps(error_data),
                            content_type='application/json',
                            status=200
                        )
                except Exception:
                    return HttpResponse(
                        json.dumps(error_data),
                        content_type='application/json',
                        status=200
                    )

    def process_response(self, request, response):
        """处理响应"""
        if self.enable and (self.methods == 'ALL' or request.method in self.methods):
            self._create_operation_log(request, response)

        # 前端接口访问控制
        if not self.IS_ALLOW_FRONTEND and FRONTEND_API_LIST:
            if any(i in request.request_path for i in FRONTEND_API_LIST):
                return HttpResponseForbidden('<h1>Access Forbidden 301</h1>')

        return response


class OperateAllowFrontendView(APIView):
    """
    超级管理员动态启用/禁用/获取 禁止前端接口访问
    优化点：
    1. 更清晰的API文档
    2. 更好的错误处理
    3. 使用DRF的响应方式
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
        获取当前是否允许前端访问的状态
        
        返回:
            SuccessResponse: 包含 is_allow 字段的响应
        """
        return SuccessResponse(
            data={'is_allow': ApiLoggingMiddleware.IS_ALLOW_FRONTEND},
            msg='success'
        )

    def post(self, request):
        """
        设置是否允许前端访问
        
        参数:
            is_allow (int): 1 允许访问, 0 禁止访问
            
        返回:
            SuccessResponse/ErrorResponse: 操作结果响应
        """
        if not request.user.is_superuser:
            return ErrorResponse(msg="您没有权限操作", status=403)
        
        try:
            is_allow = int(get_parameter_dic(request).get('is_allow', 0))
            ApiLoggingMiddleware.IS_ALLOW_FRONTEND = bool(is_allow)
            return SuccessResponse(
                data={'is_allow': ApiLoggingMiddleware.IS_ALLOW_FRONTEND},
                msg='设置成功'
            )
        except (ValueError, KeyError):
            return ErrorResponse(msg="参数错误", status=400)