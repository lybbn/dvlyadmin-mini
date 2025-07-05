# -*- coding: utf-8 -*-

"""
@Author: lybbn
@QQ:1042594286
@EditDate: 2025-06-28
@Remark: 自定义列权限
"""
from mysystem.models import MenuField,FieldPermission
from django.db.models import F
from django.core.cache import cache
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from utils.jsonResponse import SuccessResponse,DetailResponse,ErrorResponse
from config import FIELD_PERMISSION_CACHE

class FieldPermissionMixin:
    """
    字段权限控制混合类
    功能：
    1. 提供字段权限查询接口 (/field_permission/)
    2. 自动应用字段权限到序列化器
    3. 支持超级管理员自动拥有全部权限
    使用方法：
    class YourViewSet(FieldPermissionMixin, ModelViewSet):
        serializer_class = YourSerializer
    """
    # 权限缓存配置
    permission_cache_timeout = 3600  # 1小时
    permission_cache_prefix = 'lyadmin_mini_field_perm:'

    def get_permission_cache_key(self, model_name, role_ids):
        """生成缓存键"""
        sorted_roles = sorted(role_ids)
        return f"{self.permission_cache_prefix}{model_name}:{':'.join(map(str, sorted_roles))}"

    def get_field_permissions(self, request):
        """
        获取当前用户的字段权限规则（带缓存）
        返回格式: {
            "field_name": {
                "can_view": bool,
                "can_create": bool,
                "can_update": bool
            }
        }
        """
        model_name = self.serializer_class.Meta.model.__name__
        user = request.user

        # 超级管理员返回全部权限
        if getattr(user, 'is_superuser', False):
            return self.get_all_fields_permission(model_name)

        # 普通用户从缓存或数据库获取
        role_ids = tuple(user.role.values_list('id', flat=True))
        
        if FIELD_PERMISSION_CACHE:
            cache_key = self.get_permission_cache_key(model_name, role_ids)
            permissions = cache.get(cache_key)
            if permissions is None:
                permissions = self.query_database_permissions(model_name, role_ids)
                cache.set(cache_key, permissions, self.permission_cache_timeout)
        else:
            permissions = self.query_database_permissions(model_name, role_ids)
        
        return permissions

    def get_all_fields_permission(self, model_name):
        """获取所有字段的完全权限"""
        fields = MenuField.objects.filter(model=model_name).values('field_name')
        return {
            field['field_name']: {
                "can_create": True,
                "can_view": True,
                "can_update": True
            }
            for field in fields
        }

    def query_database_permissions(self, model_name, role_ids):
        """从数据库查询权限并合并"""
        queryset = FieldPermission.objects.filter(
            field__model=model_name,
            role__in=role_ids
        ).values(
            'can_create', 'can_view', 'can_update',
            field_name=F('field__field_name')
        )
        return self.merge_permissions(list(queryset))

    @staticmethod
    def merge_permissions(data):
        """
        合并多个角色的权限（OR逻辑）
        参数格式: [
            {"field_name": "name", "can_create": True, ...},
            {"field_name": "name", "can_create": False, ...}
        ]
        """
        result = {}
        for item in data:
            field_name = item['field_name']
            if field_name not in result:
                result[field_name] = item.copy()
            else:
                for perm in ['can_create', 'can_view', 'can_update']:
                    result[field_name][perm] = result[field_name][perm] or item[perm]
        return result

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def field_permission(self, request):
        """
        字段权限查询接口
        GET /your_endpoint/field_permission/
        返回示例: {
            "name": {"can_create": True, "can_view": True, "can_update": False},
            "email": {"can_create": False, "can_view": True, "can_update": True}
        }
        """
        permissions = self.get_field_permissions(request)
        return DetailResponse(data=permissions)

    def apply_field_permissions(self, serializer_class, *args, **kwargs):
        """
        动态应用字段权限到序列化器类
        
        参数:
            serializer_class: 要修改的序列化器类
            *args, **kwargs: 传递给序列化器构造函数的参数
        
        返回:
            修改后的序列化器实例
        """
        # 1. 获取请求对象
        request = kwargs.get('context', {}).get('request') or kwargs.get('request')
        if not request:
            return serializer_class(*args, **kwargs)
        
        # 2. 获取权限规则
        permissions = self.get_field_permissions(request)
        if not permissions:
            return serializer_class(*args, **kwargs)
        
        # 3. 创建动态序列化器子类
        class DynamicSerializer(serializer_class):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                
                # 处理 ListSerializer 情况
                actual_serializer = self.child if hasattr(self, 'child') else self
                
                # 获取所有字段
                fields = getattr(actual_serializer, 'fields', {})
                
                # 应用权限控制
                for field_name, field in list(fields.items()):
                    if field_name in permissions:
                        perm = permissions[field_name]
                        
                        # 无查看权限则移除字段
                        if not perm['can_view']:
                            fields.pop(field_name, None)
                            continue

                        # 控制写权限
                        if self.context.get('action') == 'create' and not perm['can_create']:
                            field.read_only = True
                        elif self.context.get('action') in ['update', 'partial_update'] and not perm['can_update']:
                            field.read_only = True
        
        # 4. 确保 action 信息传递到上下文
        kwargs.setdefault('context', {})
        kwargs['context'].setdefault('action', self.action)
        kwargs['context']['request'] = request
        
        return DynamicSerializer(*args, **kwargs)