# -*- coding: utf-8 -*-

"""
@Remark: 角色管理
"""
import django_filters
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from mysystem.models import Role, Menu
from mysystem.views.dept import DeptSerializer
from mysystem.views.menu import MenuSerializer
from mysystem.views.menu_button import MenuButtonSerializer
from utils.jsonResponse import SuccessResponse,DetailResponse,ErrorResponse
from utils.serializers import CustomModelSerializer
from rest_framework.validators import UniqueValidator
from utils.viewset import CustomModelViewSet
from utils.common import get_parameter_dic

class RoleFilterSet(django_filters.rest_framework.FilterSet):
    """
    角色管理 过滤器
    """
    #开始时间
    beginAt = django_filters.DateTimeFilter(field_name='create_datetime', lookup_expr='gte')  # 指定过滤的字段
    #结束时间
    endAt = django_filters.DateTimeFilter(field_name='create_datetime', lookup_expr='lte')
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status')

    class Meta:
        model = Role
        fields = ['beginAt', 'endAt', 'name','status']


class RoleSerializer(CustomModelSerializer):
    """
    角色-序列化器
    """

    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ["id"]


class RoleCreateUpdateSerializer(CustomModelSerializer):
    """
    角色管理 创建/更新时的列化器
    """
    dept = DeptSerializer(many=True, read_only=True)
    key = serializers.CharField(max_length=50,validators=[UniqueValidator(queryset=Role.objects.all(), message="权限字符必须唯一")])
    name = serializers.CharField(max_length=50,validators=[UniqueValidator(queryset=Role.objects.all(),message="角色名称必须唯一")])

    def validate(self, attrs: dict):
        return super().validate(attrs)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.dept.set(self.initial_data.get('dept', []))
        return data

    class Meta:
        model = Role
        fields = '__all__'


class MenuPermissonSerializer(CustomModelSerializer):
    """
    菜单的按钮权限
    """
    menuPermission = MenuButtonSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'


class RoleViewSet(CustomModelViewSet):
    """
    角色管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    create_serializer_class = RoleCreateUpdateSerializer
    update_serializer_class = RoleCreateUpdateSerializer
    filterset_class = RoleFilterSet
    search_fields = ('name', 'key')

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

    def roleId_to_menu(self, request, *args, **kwargs):
        """通过角色id获取该角色用于的菜单"""
        queryset = Menu.objects.filter(status=True).order_by("sort")
        serializer = MenuPermissonSerializer(queryset, many=True)
        return DetailResponse(data=serializer.data)

    def role_data(self,request,*args,**kwargs):
        instance = self.get_object()
        serializer = RoleSerializer(instance)
        return DetailResponse(data=serializer.data)

class PermissionViewSet(CustomModelViewSet):
    """
    角色管理-权限管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    create_serializer_class = RoleCreateUpdateSerializer
    update_serializer_class = RoleCreateUpdateSerializer
    filterset_fields = ['status']