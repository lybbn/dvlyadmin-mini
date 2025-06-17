# -*- coding: utf-8 -*-

"""
@Remark: 角色管理
"""
import django_filters
from rest_framework import serializers

from mysystem.models import Dept
from utils.jsonResponse import SuccessResponse,ErrorResponse
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet
from utils.common import get_parameter_dic

class DeptFilterSet(django_filters.rest_framework.FilterSet):
    """
    老师管理 过滤器
    """
    #开始时间
    beginAt = django_filters.DateTimeFilter(field_name='create_datetime', lookup_expr='gte')  # 指定过滤的字段
    #结束时间
    endAt = django_filters.DateTimeFilter(field_name='create_datetime', lookup_expr='lte')
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status')

    class Meta:
        model = Dept
        fields = ['beginAt', 'endAt', 'name','status']

class DeptSerializer(CustomModelSerializer):
    """
    部门-序列化器
    """

    class Meta:
        model = Dept
        fields = "__all__"
        read_only_fields = ["id"]


class DeptCreateUpdateSerializer(CustomModelSerializer):
    """
    部门管理 创建/更新时的列化器
    """

    class Meta:
        model = Dept
        fields = '__all__'


class DeptTreeSerializer(CustomModelSerializer):
    """
    部门表的树形序列化器
    """
    children = serializers.SerializerMethodField(read_only=True)

    def get_children(self, instance):
        queryset = Dept.objects.filter(parent=instance.id).filter(status=1)
        if queryset:
            serializer = DeptTreeSerializer(queryset, many=True)
            return serializer.data
        else:
            return None

    class Meta:
        model = Dept
        fields = "__all__"
        read_only_fields = ["id"]


class DeptViewSet(CustomModelViewSet):
    """
    部门管理接口:
    """
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer
    filterset_class = DeptFilterSet
    search_fields = ['name', 'owner','phone','email']

    def set_status(self,request,*args, **kwargs):
        """禁用/启用"""
        reqData = get_parameter_dic(request)
        instance = self.filter_queryset(self.get_queryset(id=reqData.get("id",""))).first()
        if instance:
            instance.status = False if instance.status else True
            instance.save()
            return SuccessResponse(data=None, msg="修改成功")
        else:
            return ErrorResponse(msg="未获取到数据")

    def dept_tree(self, request):
        queryset = Dept.objects.exclude(status=0).filter(parent=None)
        serializer = DeptTreeSerializer(queryset, many=True)
        return SuccessResponse(data=serializer.data, msg="获取成功")
