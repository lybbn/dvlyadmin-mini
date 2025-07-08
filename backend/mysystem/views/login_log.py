# -*- coding: utf-8 -*-

"""
@Remark: 操作日志管理
"""
from rest_framework import serializers
from mysystem.models import LoginLog
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet
from utils.jsonResponse import SuccessResponse, ErrorResponse
import django_filters
from django.db.models import Q

class LoginLogTimeFilter(django_filters.rest_framework.FilterSet):
    """
    登录日志 简单过滤器
    """
    #开始时间
    beginAt = django_filters.DateTimeFilter(field_name='create_datetime', lookup_expr='gte')
    #结束时间
    endAt = django_filters.DateTimeFilter(field_name='create_datetime', lookup_expr='lte')
    # 模糊搜索
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')
    # 模糊搜索
    ip = django_filters.CharFilter(field_name='ip', lookup_expr='icontains')

    class Meta:
        model = LoginLog
        fields = ['beginAt', 'endAt','username','ip']


class LoginLogSerializer(CustomModelSerializer):
    """
    登录日志-序列化器
    """

    class Meta:
        model = LoginLog
        fields = "__all__"
        read_only_fields = ["id"]

class LoginLogViewSet(CustomModelViewSet):
    """
    登录日志接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = LoginLog.objects.all().order_by('-create_datetime')
    serializer_class = LoginLogSerializer
    # filterset_fields = '__all__'
    filterset_class = LoginLogTimeFilter
    search_fields = ('ip','username')

    def getOwnerLogs(self, request, *args, **kwargs):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(Q(creator=user) | Q(username=user.username)).distinct()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    def deletealllogs(self,request):
        user = request.user
        if user.is_superuser:
            LoginLog.objects.all().delete()
            return SuccessResponse(msg="清空成功")
        return ErrorResponse(msg="您没有权限执行此操作，需要超级管理员权限")
