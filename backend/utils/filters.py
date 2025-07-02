# -*- coding: utf-8 -*-

"""
@EditDate: 2025-06-28
@Remark: 自定义过滤器
"""
from rest_framework.filters import BaseFilterBackend

from mysystem.models import Dept,MenuButton,RoleMenuButtonPermission,RoleMenuPermission

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.constants import LOOKUP_SEP
from django_filters import utils
import operator
from functools import reduce
from django.db.models import Q
from django.core.cache import cache
from config import DATA_FILTER_CACHE,DATA_FILTER_CAHCE_TIME

def get_dept_children_ids(dept_id, include_self=False):
    """
    获取部门的所有子部门ID(包括自身可选)
    使用缓存优化性能，递归获取所有层级子部门
    """
    result = None
    if DATA_FILTER_CACHE:
        cache_key = f'lyadmin_mini_dept_children:{dept_id}'
        result = cache.get(cache_key)
    
    if result is None:
        # 获取所有部门数据，避免多次查询
        dept_all_list = list(Dept.objects.filter(status=True).values('id', 'parent_id'))
        # 递归获取所有子部门
        result = _get_dept_children_recursive(dept_id, dept_all_list)
        if DATA_FILTER_CACHE:
            cache.set(cache_key, result, timeout=DATA_FILTER_CAHCE_TIME)
    
    if not include_self:
        result = [id for id in result if id != dept_id]
    
    return result

def _get_dept_children_recursive(dept_id, dept_all_list, dept_list=None):
    """
    递归获取子部门的内部方法
    """
    if dept_list is None:
        dept_list = [dept_id]
    
    for dept in dept_all_list:
        if dept.get('parent_id','') == dept_id:
            dept_list.append(dept.get('id'))
            _get_dept_children_recursive(dept['id'], dept_all_list, dept_list)
    
    return list(set(dept_list))  # 去重

class DataLevelPermissionsFilter(BaseFilterBackend):
    """
    数据级权限过滤器优化版
    
    权限级别:（5 优先级最高，以此类推）
    0 - 仅本人数据权限
    1 - 本部门数据权限
    2 - 本部门及以下数据权限
    3 - 自定义部门数据权限
    4 - 全部数据权限
    5 - 同全局数据权限

    步骤：
    0. 获取用户的部门id，没有部门则只返回自己的数据
    1. 判断过滤的数据是否有创建人所在部门 "creator" 字段,没有则返回全部
    2. 如果用户没有关联角色则返回本部门数据
    3. 根据角色的最大权限进行数据过滤(会有多个角色，进行去重取最大权限)
    3.1 判断用户是否为超级管理员角色/如果有1(所有数据) 则返回所有数据

    4. 只为仅本人数据权限时只返回过滤本人数据，并且部门为自己本部门(考虑到用户会变部门，只能看当前用户所在的部门数据)
    5. 自定数据权限 获取部门，根据部门过滤
    6. 如果具体按钮接口配置了数据权限，则优先使用此权限，否则使用菜单的数据权限（默认为全部数据权限）
    """

    def filter_queryset(self, request, queryset, view):

        # 超级管理员直接返回所有数据
        if request.user.is_superuser:
            return queryset

        # 0. 获取用户部门信息
        user = request.user
        user_dept_id = getattr(user, 'dept_id', None)
        
        # 无部门用户只能查看自己的数据
        if not user_dept_id:
            return queryset.filter(creator=user) if hasattr(queryset.model, 'creator') else queryset.none()

        # 1. 检查模型是否有归属字段
        if not hasattr(queryset.model, 'dept_belong'):
            return queryset

        # 2. 获取用户所有有效角色的数据权限
        roles = user.role.filter(status=True)
        if not roles.exists():#如果用户没有关联角色则返回本部门数据
            return queryset.filter(dept_belong_id=user_dept_id)
        
        role_ids = roles.values_list('id', flat=True)

        api = request.path  # 当前请求的URL路径
        method = request.method  # 当前HTTP请求方法
        methodList = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
        method = methodList.index(method)
        re_api = api  # 默认使用原始路径

        # 从URL参数中提取主键`pk`（如果存在）
        _upk = request.parser_context["kwargs"].get('pk')
        if _upk:  # 如果URL中包含主键
            re_api = re_api.replace(str(_upk), '{id}')  # 将`pk`替换为`{id}`

        # 3. 处理数据权限
        # 先匹配接口数据权限，如果按钮接口配置了数据权限优先处理
        menu_button_ids = []
        menu_ids = []

        menu_button_data = MenuButton.objects.filter(api=re_api, method=method).values_list('id', 'menu_id', named=True)
        if menu_button_data:
            menu_button_ids = [item.id for item in menu_button_data]
            menu_ids = [item.menu_id for item in menu_button_data]
        
        role_permissions = []
        if menu_button_ids:
            # 获取角色按钮权限数据（合并查询条件）
            role_permissions = RoleMenuButtonPermission.objects.filter(
                role__in=role_ids,
                menu_button_id__in=menu_button_ids
            ).values('data_scope')

        max_data_scope = self._get_max_data_scope(role_permissions)
        is_menu = False
        if max_data_scope in [5,-1]: #按钮数据权限未配置则按本菜单的全局数据权限策略处理
            is_menu = True
            if menu_ids:
                # 获取角色菜单权限数据（合并查询条件）
                role_menu_permissions = RoleMenuPermission.objects.filter(
                    role__in=role_ids,
                    menu_id__in=menu_ids
                ).values('data_scope')
                max_data_scope = self._get_max_data_scope(role_menu_permissions)
            else:
                max_data_scope = 4 # 菜单数据权限默认【全部数据权限】
        
        # 3.1 最高权限直接返回
        if max_data_scope == 4:  # 全部数据权限
            return queryset
        
        # 4. 处理各权限级别
        if max_data_scope == 0:  # 仅本人数据
            return queryset.filter(creator=user)
        
        # 5. 获取需要过滤的部门列表
        dept_ids = self._get_permitted_dept_ids(user_dept_id, role_ids, max_data_scope,is_menu=is_menu)
        
        # 6. 应用部门过滤
        if queryset.model._meta.model_name == 'dept':
            return queryset.filter(id__in=dept_ids)
        return queryset.filter(dept_belong__in=dept_ids)

    def _get_max_data_scope(self, role_permissions):
        """获取用户拥有的最大数据权限范围"""
        data_scopes = []
        for i in role_permissions:
            data_scopes.append(i.get("data_scope"))
        data_scopes = list(set(data_scopes))#去重
        return max(data_scopes) if data_scopes else -1  # 默认为-1

    def _get_permitted_dept_ids(self, user_dept_id, role_ids, max_data_scope,is_menu=True):
        """
        根据权限级别获取允许访问的部门ID列表
        is_menu:是否使用菜单的数据权限
        """
        dept_ids = set()
        
        if max_data_scope == 1:  # 本部门
            dept_ids.add(user_dept_id)
        elif max_data_scope == 2:  # 本部门及以下
            dept_ids.update(get_dept_children_ids(user_dept_id, include_self=True))
        elif max_data_scope == 3:  # 自定义部门
            if is_menu:
                custom_depts = RoleMenuPermission.objects.filter(role__in=role_ids,data_scope=3).values_list('dept__id',flat=True)
            else:
                custom_depts = RoleMenuButtonPermission.objects.filter(role__in=role_ids,data_scope=3).values_list('dept__id',flat=True)
            dept_ids.update(custom_depts)
        
        return list(dept_ids) if dept_ids else [user_dept_id]  # 默认至少包含本部门

class CustomDjangoFilterBackend(DjangoFilterBackend):
    lookup_prefixes = {
        '^': 'istartswith',
        '=': 'iexact',
        '@': 'search',
        '$': 'iregex',
        '~': 'icontains'
    }

    def construct_search(self, field_name, lookup_expr=None):
        lookup = self.lookup_prefixes.get(field_name[0])
        if lookup:
            field_name = field_name[1:]
        else:
            lookup = lookup_expr
        if lookup:
            if field_name.endswith(lookup):
                return field_name
            return LOOKUP_SEP.join([field_name, lookup])
        return field_name

    def find_filter_lookups(self, orm_lookups, search_term_key):
        for lookup in orm_lookups:
            new_lookup = LOOKUP_SEP.join(lookup.split(LOOKUP_SEP)[:-1]) if len(lookup.split(LOOKUP_SEP)) > 1 else lookup
            if new_lookup == search_term_key:
                return lookup
        return None

    def filter_queryset(self, request, queryset, view):
        filterset = self.get_filterset(request, queryset, view)
        if filterset is None:
            return queryset
        if filterset.__class__.__name__ == "AutoFilterSet":
            queryset = filterset.queryset
            filter_fields = filterset.filters if self.filter_fields == "__all__" else self.filter_fields
            orm_lookup_dict = dict(
                zip(
                    [field for field in filter_fields],
                    [filterset.filters[lookup].lookup_expr for lookup in filterset.filters.keys()],
                )
            )
            orm_lookups = [self.construct_search(lookup, lookup_expr) for lookup, lookup_expr in orm_lookup_dict.items()]
            conditions = []
            queries = []
            for search_term_key in filterset.data.keys():
                orm_lookup = self.find_filter_lookups(orm_lookups, search_term_key)
                if not orm_lookup or filterset.data.get(search_term_key) == '':
                    continue
                filterset_data_len = len(filterset.data.getlist(search_term_key))
                if filterset_data_len == 1:
                    query = Q(**{orm_lookup: filterset.data[search_term_key]})
                    queries.append(query)
                elif filterset_data_len == 2:
                    orm_lookup += '__range'
                    query = Q(**{orm_lookup: filterset.data.getlist(search_term_key)})
                    queries.append(query)
            if len(queries) > 0:
                conditions.append(reduce(operator.and_, queries))
                queryset = queryset.filter(reduce(operator.and_, conditions))
                return queryset
            else:
                return queryset

        if not filterset.is_valid() and self.raise_exception:
            raise utils.translate_validation(filterset.errors)
        return filterset.qs