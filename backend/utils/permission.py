# -*- coding: utf-8 -*-

"""
@Author: lybbn
@QQ :1042594286
@Version: 1.0
@EditDate: 2025-07-02
@Remark: 自定义权限验证模块
"""
import re
import json
from django.core.cache import cache
from rest_framework.permissions import BasePermission
from django.db.models import F, Q
from config import IS_DEMO,CUSTOM_PERMISSION_CAHCE,CUSTOM_PERMISSION_CAHCE_TIME,CUSTOM_PERMISSION_WHITELIST
from mysystem.models import RoleMenuButtonPermission
from rest_framework.exceptions import PermissionDenied
from mysystem.models import SystemConfig

class APIPermissionValidator:
    """API权限验证工具类"""
    # 是否启用缓存
    CAN_CACHE = CUSTOM_PERMISSION_CAHCE
    # 缓存超时时间
    CACHE_TIMEOUT = CUSTOM_PERMISSION_CAHCE_TIME 
    
    @staticmethod
    def validate_api_path(request_path: str, permission_api: str) -> bool:
        """
        使用正则验证请求路径是否匹配权限路径
        :param request_path: 当前请求路径
        :param permission_api: 权限配置的API路径
        :return: 是否匹配
        """
        if not permission_api:
            return False
            
        # 将{id}等路径参数转换为正则表达式
        pattern = permission_api.replace('{id}', r'.*?').replace('/', r'\/')
        return bool(re.fullmatch(pattern, request_path))

    @classmethod
    def get_user_permissions(cls, user_id,role_ids):
        """
        获取用户权限数据（使用Django缓存）
        :param user_id: 用户ID
        :param role_ids: 用户角色id列表
        :return: 权限列表 (api, method)
        """
        permissions = None
        if APIPermissionValidator.CAN_CACHE:
            cache_key = f"lyadmin_mini_user_permissions_{user_id}"
            permissions = cache.get(cache_key)
        
        if permissions is None:
            # 缓存未命中，从数据库查询
            permissions = set(
                RoleMenuButtonPermission.objects
                .filter(role__in=role_ids)
                .values_list('menu_button__api', 'menu_button__method')
            )
            if APIPermissionValidator.CAN_CACHE:
                # 设置缓存
                cache.set(cache_key, permissions, cls.CACHE_TIMEOUT)
            
        return permissions

    @classmethod
    def clear_user_permissions_cache(cls, user_id = None, is_all = False):
        """
        清除用户权限缓存（当用户权限变更时调用）
        :param user_id: 用户ID
        :param is_all : 是否清理所有的
        """
        if not is_all:
            cache_key = f"lyadmin_mini_user_permissions_{user_id}"
            cache.delete(cache_key)
        else:
            keys = cache.keys("lyadmin_mini_user_permissions_*")
            if keys:
                cache.delete_many(keys)

class CustomPermission(BasePermission):
    """优化后的自定义权限验证"""
    
    # 演示模式白名单（只读接口）
    DEMO_WHITELIST = {
        ('/api/lyformbuilder/lyformbuilder/previewcodejson/', 'POST'),
        ('/api/mall/goodsspu/export/', 'POST')
    }

    # 生产白名单

    WHITELIST = CUSTOM_PERMISSION_WHITELIST
    
    def has_permission(self, request, view):

         # 超级管理员放行
        if request.user.is_superuser:
            return True
        
        # 白名单
        if self._check_whitelist(request):
            return True

        # 演示模式检查
        if self._is_demo_mode_blocked(request):
            return False
            
        # 检查视图是否豁免权限
        if self._is_view_step_permission(view):
            return True
            
        # 验证API权限
        return self._check_api_permission(request)
    
    def _check_demo_whitelist(self, request) -> bool:
        """检查请求是否在演示白名单中"""
        current_path = request.path
        current_method = request.method
        
        for (whitelist_path, whitelist_method) in self.DEMO_WHITELIST:
            # 方法不匹配则跳过
            if current_method != whitelist_method:
                continue
                
            # 精确匹配完整路径
            if current_path == whitelist_path:
                return True
                
            # 处理带{id}的路径匹配
            if '{id}' in whitelist_path:
                # 将白名单路径转换为正则表达式
                if self._match_param_path(whitelist_path,current_path):
                    return True
                    
        return False
    
    def _combine_whitelists(self,config_whitelist, db_whitelist):
        """
        合并配置白名单和数据库白名单，处理所有边界情况
        :param config_whitelist: 配置中的白名单，格式为 { (path, method), ... } 或 [ (path, method), ... ]
        :param db_whitelist: 数据库中的白名单，格式为 [ (path, method), ... ] 或 None
        :return: 合并后的白名单集合 set( (path, method), ... )
        """
        # 处理 config_whitelist
        config_set = set(config_whitelist) if config_whitelist else set()
        
        # 处理 db_whitelist
        db_set = set(db_whitelist) if db_whitelist else set()
        
        # 合并并返回
        return config_set.union(db_set)
    
    def _check_whitelist(self, request) -> bool:
        """检查请求是否在白名单中"""
        current_path = request.path
        current_method = request.method.upper()
        
        db_whitelist = self._get_db_whitelist()

        # 合并config和数据库的白名单
        combined_whitelist = self._combine_whitelists(self.WHITELIST,db_whitelist)

        for (whitelist_path, whitelist_method) in combined_whitelist:
            # 方法不匹配则跳过
            if current_method != whitelist_method or not whitelist_method == "ALL":
                continue
                
            # 精确匹配完整路径
            if current_path == whitelist_path:
                return True
                
            # 处理带{id}的路径匹配
            if '{id}' in whitelist_path:
                # 将白名单路径转换为正则表达式
                if self._match_param_path(whitelist_path,current_path):
                    return True
                    
        return False

    def safe_parse_json(self,value):
        try:
            # 处理可能的外层引号
            if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            return json.loads(value)
        except json.JSONDecodeError:
            return None
    
    def _get_db_whitelist(self):
        """从数据库获取白名单列表（带缓存）"""
        whitelist = []
        if CUSTOM_PERMISSION_CAHCE:
            cache_key = 'api_whitelist_cache'
            whitelist = cache.get(cache_key)
        wlist = []
        if whitelist is None:
            ins = SystemConfig.objects.filter(key="apiWhiteList").first()
            if not ins:
                return []
            else:
                wlist = self.safe_parse_json(ins.value)
            if wlist:
                whitelist = [(item.api, item.method) for item in wlist]
                if CUSTOM_PERMISSION_CAHCE:
                    cache.set(cache_key, whitelist, timeout=CUSTOM_PERMISSION_CAHCE_TIME)
            else:
                return []
        
        return whitelist

    def _is_demo_mode_blocked(self, request) -> bool:
        """检查演示模式限制"""
        if not IS_DEMO:
            return False
        
        if self._check_demo_whitelist(request):
            return False
            
        # 演示模式下阻止非白名单的修改操作
        if request.method not in ('GET', 'HEAD', 'OPTIONS'):
            raise PermissionDenied('演示环境禁止修改操作')
        return False

    def _is_view_step_permission(self, view) -> bool:
        """检查视图是否不需要权限控制"""
        # 检查视图或特定方法是否标记为无需权限
        view_action = getattr(view, 'action', None)
        if view_action:
            action_method = getattr(view, view_action, None)
            if action_method and getattr(action_method, 'step_permission', False):
                return True
                
        return getattr(view, 'step_permission', False)

    def _check_api_permission(self, request) -> bool:
        """核心权限验证逻辑"""
        # 无角色用户拒绝
        if not hasattr(request.user, 'role'):
            return False
            
        # 获取用户所有权限（使用缓存）
        role_ids = request.user.role.values_list('id', flat=True)
        user_permissions = APIPermissionValidator.get_user_permissions(request.user.id,role_ids)
        
        # 检查当前请求是否匹配任一权限
        current_api = request.path
        current_method = request.method
        methodList = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
        current_method = methodList.index(current_method)
        
        for perm_api, perm_method in user_permissions:
            if (current_method == perm_method and 
                APIPermissionValidator.validate_api_path(current_api, perm_api)):
                return True
                
        return False
    
    def _match_param_path(self, pattern_path: str, request_path: str) -> bool:
        """
        匹配含参数的路径（支持多种参数类型）
        
        参数:
            pattern_path: 配置的白名单路径模式，如 '/api/items/{id}/'
            request_path: 实际请求的路径，如 '/api/items/123/'
        
        返回:
            bool: 是否匹配成功
        """
        pattern = pattern_path.replace('{id}', r'([a-zA-Z0-9-]+)').replace('/', r'\/')
        if re.fullmatch(pattern, request_path):
            return True
        return False
    
# # 使用示例：在视图中标记无需自定义权限的方法
# class SomeViewSet(viewsets.ModelViewSet):
#     permission_classes = [CustomPermission]

#     @action(detail=False, methods=['get'], step_permission=True)
#     def public_list(self, request):
#         """无需权限的公开接口"""
#         ...