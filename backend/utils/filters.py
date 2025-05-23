# -*- coding: utf-8 -*-

"""
@Remark: 自定义过滤器
"""
import re
from rest_framework.filters import BaseFilterBackend

from mysystem.models import Dept,RoleMenuDataRange,MenuButton

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.constants import LOOKUP_SEP
from django_filters import utils
import six
from django_filters.filters import CharFilter
import operator
from functools import reduce
from django.db.models import Q


def get_dept(dept_id, dept_all_list=None, dept_list=None):
    """
    递归获取部门的所有下级部门
    :param dept_id: 需要获取的部门id
    :param dept_all_list: 所有部门列表
    :param dept_list: 递归部门list
    :return:
    """
    if not dept_all_list:
        dept_all_list = Dept.objects.all().values('id', 'parent')
    if dept_list is None:
        dept_list = [dept_id]
    for ele in dept_all_list:
        if ele.get('parent') == dept_id:
            dept_list.append(ele.get('id'))
            get_dept(ele.get('id'), dept_all_list, dept_list)
    return list(set(dept_list))

def getApiMenuList(request):
    """
    根据请求接口获取对应菜单列表（一个接口可能配置到多个菜单中），要严格控制，建议一个接口配置到一个菜单中
    :param request: 当前请求
    :return: []
    """
    menu_id_list = []
    reqApi = request.path
    ApiList = MenuButton.objects.filter(api__isnull = False).exclude(api = '').values("api","method","menu_id")
    for a in ApiList:
        validApi = a.get('api')
        valid_api = validApi.replace('{id}', '.*?')
        matchObj = re.match(valid_api, reqApi, re.M | re.I)
        if matchObj:
            menu_id_list.append(a.get('menu_id'))
    return list(set(menu_id_list))

class DataLevelPermissionsFilter(BaseFilterBackend):
    """
    数据 级权限过滤器
    0. 获取用户的部门id，没有部门则返回空
    1. 判断过滤的数据是否有创建人所在部门 "creator" 字段,没有则返回全部
    2. 如果用户没有关联角色则返回本部门数据
    3. 根据角色的最大权限进行数据过滤(会有多个角色，进行去重取最大权限)
    3.1 判断用户是否为超级管理员角色/如果有1(所有数据) 则返回所有数据

    4. 只为仅本人数据权限时只返回过滤本人数据，并且部门为自己本部门(考虑到用户会变部门，只能看当前用户所在的部门数据)
    5. 自定数据权限 获取部门，根据部门过滤
    """

    def filter_queryset(self, request, queryset, view):
        """
        判断是否为超级管理员:
        如果不是超级管理员,则进入下一步权限判断
        """
        if request.user.is_superuser == 0:
            # 0. 获取用户的部门id，没有部门则返回空
            user_dept_id = getattr(request.user, 'dept_id', None)
            if not user_dept_id:
                return queryset.none()

            # 1. 判断过滤的数据是否有创建人所在部门 "dept_belong_id" 字段
            if not getattr(queryset.model, 'dept_belong_id', None):
                return queryset

            # 2. 如果用户没有关联角色则返回本部门数据
            if not hasattr(request.user, 'role'):
                return queryset.filter(dept_belong_id=user_dept_id)

            # 菜单数据权限
            lypageList = getApiMenuList(request)
            menu_dataScope_list = []
            # 3. 根据所有角色 获取所有权限范围
            role_list = request.user.role.filter(status=1).values('id','admin', 'data_range')
            role_ids = []
            dataScope_list = []
            for ele in role_list:
                role_ids.append(ele.get('id'))
                # 3.1 判断用户是否为超级管理员角色/如果有1(所有数据) 则返回所有数据
                # if 3 == ele.get('data_range') or ele.get('admin') == True:#该权限已禁用，默认系统只能有一个超级管理员
                # if 3 == ele.get('data_range'):
                #     return queryset
                dataScope_list.append(ele.get('data_range'))
            dataScope_list = list(set(dataScope_list))
            if lypageList:
                menu_dataScope_list = list(set(RoleMenuDataRange.objects.filter(role_id__in=role_ids,menu_id__in=lypageList).values_list("data_range",flat=True)))
            if 3 in dataScope_list:#全局全部数据权限-菜单数据权限-放通全部数据权限
                if 5 in menu_dataScope_list or 3 in menu_dataScope_list or not menu_dataScope_list:
                    return queryset
                if 0 in menu_dataScope_list:
                    return queryset.filter(creator=request.user, dept_belong_id=user_dept_id)
                dept_list = []
                if 1 in menu_dataScope_list or 2 in menu_dataScope_list:
                    for role_menu_datarange in menu_dataScope_list:
                        if role_menu_datarange == 2:#"本部门及以下数据权限"
                            dept_list.extend(get_dept(user_dept_id, ))
                        elif role_menu_datarange == 1:#"本部门数据权限"
                            dept_list.append(user_dept_id)

                    return queryset.filter(dept_belong_id__in=list(set(dept_list)))
            # 4. 只为仅本人数据权限时只返回过滤本人数据，并且部门为自己本部门(考虑到用户会变部门，只能看当前用户所在的部门数据)
            if 0 in dataScope_list:
                if menu_dataScope_list:
                    if 3 in menu_dataScope_list:
                        return queryset
                    elif 1 in menu_dataScope_list or 2 in menu_dataScope_list:
                        dept_list = []
                        for role_menu_datarange in menu_dataScope_list:
                            if role_menu_datarange == 2:#"本部门及以下数据权限"
                                dept_list.extend(get_dept(user_dept_id, ))
                            elif role_menu_datarange == 1:#"本部门数据权限"
                                dept_list.append(user_dept_id)
                        return queryset.filter(dept_belong_id__in=list(set(dept_list)))
                #不存在菜单数据权限和菜单数据权限为0和5时则为仅本人数据权限
                return queryset.filter(creator=request.user, dept_belong_id=user_dept_id)

            # 5. 自定义数据权限 获取部门，根据部门过滤
            dept_list = []
            for ele in dataScope_list:
                if ele == 4:#自定义数据权限会读取role里面的dept部门
                    if menu_dataScope_list:
                        if 3 in menu_dataScope_list:
                            return queryset
                        elif 0 in menu_dataScope_list:
                            return queryset.filter(creator=request.user, dept_belong_id=user_dept_id)
                        elif 1 in menu_dataScope_list or 2 in menu_dataScope_list:
                            for role_menu_datarange in menu_dataScope_list:
                                if role_menu_datarange == 2:#"本部门及以下数据权限"
                                    dept_list.extend(get_dept(user_dept_id, ))
                                elif role_menu_datarange == 1:#"本部门数据权限"
                                    dept_list.append(user_dept_id)
                        else:
                            dept_list.extend(request.user.role.filter(status=1).values_list('dept__id', flat=True))
                    else:
                        dept_list.extend(request.user.role.filter(status=1).values_list('dept__id', flat=True))
                elif ele == 2:#"本部门及以下数据权限"
                    if menu_dataScope_list:
                        if 3 in menu_dataScope_list:
                            return queryset
                        elif 0 in menu_dataScope_list:
                            return queryset.filter(creator=request.user, dept_belong_id=user_dept_id)
                        elif 1 in menu_dataScope_list:
                            dept_list.append(user_dept_id)
                        else:
                            dept_list.extend(get_dept(user_dept_id, ))
                    else:
                        dept_list.extend(get_dept(user_dept_id, ))
                elif ele == 1:#"本部门数据权限"
                    if menu_dataScope_list:
                        if 3 in menu_dataScope_list:
                            return queryset
                        elif 0 in menu_dataScope_list:
                            return queryset.filter(creator=request.user, dept_belong_id=user_dept_id)
                        elif 2 in menu_dataScope_list:
                            dept_list.extend(get_dept(user_dept_id, ))
                        else:
                            dept_list.append(user_dept_id)
                    else:
                        dept_list.append(user_dept_id)
            if queryset.model._meta.model_name == 'dept':
                return queryset.filter(id__in=list(set(dept_list)))
            return queryset.filter(dept_belong_id__in=list(set(dept_list)))
        else:
            return queryset


class CustomDjangoFilterBackend(DjangoFilterBackend):
    lookup_prefixes = {
        '^': 'istartswith',
        '=': 'iexact',
        '@': 'search',
        '$': 'iregex',
        '~': 'icontains'
    }

    def construct_search(self, field_name):
        lookup = self.lookup_prefixes.get(field_name[0])
        if lookup:
            field_name = field_name[1:]
        else:
            lookup = 'icontains'
        return LOOKUP_SEP.join([field_name, lookup])

    def find_filter_lookups(self, orm_lookups, search_term_key):
        for lookup in orm_lookups:
            if lookup.find(search_term_key) >= 0:
                return lookup
        return None

    def filter_queryset(self, request, queryset, view):
        filterset = self.get_filterset(request, queryset, view)
        if filterset is None:
            return queryset
        if filterset.__class__.__name__ == 'AutoFilterSet':
            queryset = filterset.queryset
            orm_lookups = []
            for search_field in filterset.filters:
                if isinstance(filterset.filters[search_field],CharFilter):
                    orm_lookups.append(self.construct_search(six.text_type(search_field)))
                else:
                    orm_lookups.append(search_field)
            conditions = []
            queries = []
            for search_term_key in filterset.data.keys():
                orm_lookup = self.find_filter_lookups(orm_lookups, search_term_key)
                if not orm_lookup:
                    continue
                query = Q(**{orm_lookup: filterset.data[search_term_key]})
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