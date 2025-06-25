# -*- coding: utf-8 -*-

"""
@Remark: 部门管理
"""
import django_filters
from rest_framework import serializers

from mysystem.models import Dept
from utils.jsonResponse import SuccessResponse,ErrorResponse,DetailResponse
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet
from utils.common import get_parameter_dic

class DeptFilterSet(django_filters.rest_framework.FilterSet):
    """
    部门管理 过滤器
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

class DeptViewSet(CustomModelViewSet):
    """
    部门管理接口:
    """
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer
    filterset_class = DeptFilterSet
    search_fields = ['name', 'owner','phone','email']
    import_field_dict={
        "ID":"id",
        "部门名称": {'field': 'name', 'example': '技术部门'},
        "权限字符": {'field': 'key', 'example': 'tec'},
        "排序":{'field': 'sort', 'example': 10},
        "上级部门":"parent",
        "状态":{'field': 'status', 'example': True}
    }
    import_serializer_class = DeptSerializer

    def set_status(self,request,*args, **kwargs):
        """禁用/启用"""
        reqData = get_parameter_dic(request)
        id=reqData.get("id","")
        queryset = self.filter_queryset(self.get_queryset())
        instance = queryset.filter(id=id).first()
        if instance:
            instance.status = False if instance.status else True
            instance.save()
            return DetailResponse(data=None, msg="设置成功")
        else:
            return ErrorResponse(msg="未获取到数据")