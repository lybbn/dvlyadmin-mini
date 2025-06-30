# -*- coding: utf-8 -*-

"""
@Remark: 用户管理
"""
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from mysystem.models import Users,Role
from utils.jsonResponse import SuccessResponse, ErrorResponse,DetailResponse
from utils.permission import CustomPermission
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.validators import UniqueValidator
import django_filters
from utils.common import get_parameter_dic
from django.db import transaction

class UsersManageTimeFilter(django_filters.rest_framework.FilterSet):
    """
    用户管理 简单过滤器
    """
    #开始时间
    beginAt = django_filters.DateTimeFilter(field_name='create_datetime', lookup_expr='gte')
    #结束时间
    endAt = django_filters.DateTimeFilter(field_name='create_datetime', lookup_expr='lte')
    # 模糊搜索
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')
    # 模糊搜索
    nickname = django_filters.CharFilter(field_name='nickname', lookup_expr='icontains')
    # 模糊搜索
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    # 模糊搜索
    mobile = django_filters.CharFilter(field_name='mobile', lookup_expr='icontains')
    is_active = django_filters.CharFilter(field_name='is_active')
    dept_id = django_filters.CharFilter(field_name='dept_id')

    class Meta:
        model = Users
        fields = ['beginAt', 'endAt','username','mobile','is_active','nickname','name','dept_id']


class UserSerializer(CustomModelSerializer):
    """
    用户管理-序列化器
    """
    roleNames = serializers.SerializerMethodField(read_only=True)  # 新增自定义字段
    deptName = serializers.SerializerMethodField(read_only=True)  # 新增自定义字段

    def get_deptName(self,obj):
        try:
            return obj.dept.name
        except:
            return ""

    def get_roleNames(self,obj):
        return list(obj.role.values_list('name', flat=True))

    class Meta:
        model = Users
        read_only_fields = ["id"]
        exclude = ['password']


class UserCreateSerializer(CustomModelSerializer):
    """
    管理员用户新增-序列化器
    """
    username = serializers.CharField(max_length=50,validators=[UniqueValidator(queryset=Users.objects.all(), message="账号必须唯一")])
    password = serializers.CharField(required=False, default=make_password("123456"))

    is_staff = serializers.BooleanField(required=False,default=True)#是否允许登录后台

    def create(self, validated_data):
        if "password" in validated_data.keys():
            if validated_data['password']:
                validated_data['password'] = make_password(validated_data['password'])
        validated_data['identity'] = 1
        return super().create(validated_data)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        return data

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id"]


class UserUpdateSerializer(CustomModelSerializer):
    """
    用户修改-序列化器
    """
    username = serializers.CharField(max_length=50,validators=[UniqueValidator(queryset=Users.objects.all(), message="账号必须唯一")])
    password = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        if "password" in validated_data.keys():
            if validated_data['password']:
                validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance,validated_data)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        return data

    class Meta:
        model = Users
        read_only_fields = ["id"]
        fields = "__all__"


class UserViewSet(CustomModelViewSet):
    """
    后台管理员用户接口:
    """
    queryset = Users.objects.filter(identity=1,is_delete=False).order_by('-create_datetime')
    serializer_class = UserSerializer
    create_serializer_class = UserCreateSerializer
    update_serializer_class = UserUpdateSerializer
    # filterset_fields = ('name','is_active','username')
    filterset_class = UsersManageTimeFilter

    def set_status(self,request,*args, **kwargs):
        """禁用/启用"""
        reqData = get_parameter_dic(request)
        id=reqData.get("id","")
        queryset = self.filter_queryset(self.get_queryset())
        instance = queryset.filter(id=id).first()
        if instance:
            instance.is_active = False if instance.is_active else True
            instance.save()
            return DetailResponse(data=None, msg="设置成功")
        else:
            return ErrorResponse(msg="未获取到数据")

    def user_info(self,request):
        """获取当前用户信息"""
        user = request.user
        if not user.identity in [0,1]:return ErrorResponse(msg="用户类型错误")
        result = {
            "avatar":user.avatar,
            "nickname":user.nickname,
            "name":user.name,
            "mobile":user.mobile,
            "gender":user.gender,
            "email":user.email,
        }
        return DetailResponse(data=result,msg="获取成功")

    def update_user_info(self,request):
        """修改当前用户信息"""
        user = request.user
        if not user.identity in [0,1]:return ErrorResponse(msg="用户类型错误")
        Users.objects.filter(id=user.id).update(**request.data)
        return DetailResponse(data=None, msg="修改成功")
    
    def reset_password(self, request, pk):
        """重置用户密码
        
        Args:
            request: HTTP请求对象
            pk: 用户主键ID
            
        Returns:
            Response: 操作结果响应
        """
        # 1. 权限验证
        if not request.user.is_superuser:
            return ErrorResponse(msg="只允许超级管理员进行密码重置操作")
        
        try:
            # 2. 获取用户实例
            user = Users.objects.get(id=pk)
            
            data = request.data
            new_pwd = data.get('newPassword')
            user.password = make_password(new_pwd)
            # 3. 保存
            with transaction.atomic():
                user.save()
            
            # 4. 返回成功响应
            return DetailResponse(msg="设置成功")
            
        except Users.DoesNotExist:
            return ErrorResponse(msg="指定用户不存在")
        except Exception as e:
            return ErrorResponse(msg=f"密码重置错误：{str(e)}")


    def change_password(self,request,*args, **kwargs):
        """密码修改"""
        user = request.user
        if not user.identity in [0,1]:return ErrorResponse(msg="用户类型错误")
        instance = Users.objects.filter(id=user.id,identity__in=[0,1]).first()
        data = request.data
        old_pwd = data.get('oldPassword')
        new_pwd = data.get('newPassword')
        new_pwd2 = data.get('newPassword2')
        if instance:
            if new_pwd != new_pwd2:
                return ErrorResponse(msg="2次密码不匹配")
            elif instance.check_password(old_pwd):
                instance.password = make_password(new_pwd)
                instance.save()
                return DetailResponse(data=None, msg="修改成功")
            else:
                return ErrorResponse(msg="旧密码不正确")
        else:
            return ErrorResponse(msg="未获取到用户")
