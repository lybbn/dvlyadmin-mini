# -*- coding: utf-8 -*-

"""
@Remark: 字典管理
"""
import django_filters
from rest_framework.views import APIView
from rest_framework import serializers
from mysystem.models import Dictionary
from utils.jsonResponse import SuccessResponse,ErrorResponse,DetailResponse
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet
from utils.common import get_parameter_dic

class DictionaryFilterset(django_filters.rest_framework.FilterSet):
    """
    过滤器
    """
    parent_isnull = django_filters.BooleanFilter(field_name='parent', lookup_expr="isnull")

    class Meta:
        model = Dictionary
        fields = ['id', 'label', 'status', 'parent_isnull','parent','value']

class DictionarySerializer(CustomModelSerializer):
    """
    字典-序列化器
    """

    class Meta:
        model = Dictionary
        fields = "__all__"
        read_only_fields = ["id"]

class DictionaryViewSet(CustomModelViewSet):
    """
    字典管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Dictionary.objects.all()
    serializer_class = DictionarySerializer
    filterset_class = DictionaryFilterset
    search_fields = ('label','value')

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


class GetDictionaryInfoView(APIView):
    """
    get:
    获取字典信息
    参数：code 分组编码（value）
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        code = get_parameter_dic(request)['code']
        if not all([code]):
            return ErrorResponse(msg="params error")
        queryset = Dictionary.objects.filter(parent__value = code,status=True).order_by("sort")
        data = []
        if queryset:
            for m in queryset:
                data.append({
                    'id':m.id,
                    'label':m.label,
                    'value':m.value
                })
        return DetailResponse(data=data)

class GetDictionaryAllView(APIView):
    """
    获取字典
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        queryset = Dictionary.objects.filter(parent__isnull = True,status=True).order_by("sort")
        data = []
        for instance in queryset:
            data.append(
                {
                    "id": instance.id,
                    "label": instance.label,
                    "value": instance.value,
                    "children": list(
                        Dictionary.objects.filter(parent=instance.id).filter(status=True).order_by("sort").values("id","label", "value")
                    ),
                }
            )
        return SuccessResponse(data=data, msg="获取成功",total=len(data))