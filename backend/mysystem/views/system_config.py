import json
from rest_framework.views import APIView
from utils.jsonResponse import SuccessResponse,ErrorResponse,DetailResponse
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
import django_filters
from django.conf import settings
from django.db.models import Q
from mysystem.models import SystemConfig
from utils.common import get_parameter_dic,get_full_image_url,ast_convert
from utils.models import get_all_models_objects

def safe_parse_json(value):
    try:
        # 处理可能的外层引号
        if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        return json.loads(value)
    except json.JSONDecodeError:
        return None

class SystemConfigFilter(django_filters.rest_framework.FilterSet):
    """
    过滤器
    """
    parent__isnull = django_filters.BooleanFilter(field_name='parent', lookup_expr="isnull")

    class Meta:
        model = SystemConfig
        fields = ['id', 'parent', 'status', 'parent__isnull']

class SystemConfigSerializer(CustomModelSerializer):
    """
    系统配置-序列化器
    """
    form_item_type_label = serializers.CharField(source='get_form_item_type_display', read_only=True)

    def to_representation(self, instance):  # 序列化
        ret = super().to_representation(instance)
        ret['rule'] = ast_convert(ret['rule'])  # 可以保存的修改字段值的方法
        ret['setting'] = ast_convert(ret['setting'])
        ret['data_options'] = ast_convert(ret['data_options']) 
        return ret
    
    class Meta:
        model = SystemConfig
        fields = "__all__"
        read_only_fields = ["id"]

class SystemConfigCreateSerializer(CustomModelSerializer):
    """
    系统配置-新增时使用-序列化器
    """
    form_item_type_label = serializers.CharField(source='get_form_item_type_display', read_only=True)
    rule = serializers.JSONField(allow_null=True,required=False)
    data_options = serializers.JSONField(allow_null=True,required=False)
    setting = serializers.JSONField(allow_null=True,required=False)

    class Meta:
        model = SystemConfig
        fields = "__all__"
        read_only_fields = ["id"]

    def validate_key(self, value):
        """
        验证key是否允许重复
        parent为空时不允许重复,反之允许
        """
        instance = SystemConfig.objects.filter(key=value, parent__isnull=True).exists()
        if instance:
            raise ValueError('已存在相同变量名')
        return value

def boolValue(val):
    if isinstance(val, bool):
        return val
    if not val:
        return False
    elif val.lower() in ["true","1", 't', 'y', 'yes', 'on']:
        return True
    elif val.lower() in ["false","0", 'f', 'n', 'no', 'off']:
        return False
    else:
        raise ValueError(f"Cannot convert '{val}' to boolean")
    

class SystemConfigChildrenSerializer(CustomModelSerializer):
    """
    系统配置子级-序列化器
    """
    children = serializers.SerializerMethodField()
    form_item_type_label = serializers.CharField(source='get_form_item_type_display', read_only=True)

    def get_children(self, instance):
        queryset = SystemConfig.objects.filter(parent=instance)
        serializer = SystemConfigSerializer(queryset, many=True)
        return serializer.data

    def to_representation(self, instance):  # 序列化
        ret = super().to_representation(instance)
        ret['rule'] = ast_convert(ret['rule'])  # 可以保存的修改字段值的方法
        ret['setting'] = ast_convert(ret['setting'])  # 可以保存的修改字段值的方法
        ret['data_options'] = ast_convert(ret['data_options'])  # 可以保存的修改字段值的方法
        if ret['form_item_type']  == 9:
            ret['value'] = boolValue(ret['value'])
        if ret['key'] == "apiWhiteList":
            ret['value'] = safe_parse_json(ret['value'])
        return ret

    class Meta:
        model = SystemConfig
        fields = "__all__"
        read_only_fields = ["id"]

class SystemConfigUpdateSerializer(CustomModelSerializer):
    """
    系统配置-编辑时使用-序列化器
    """
    form_item_type_label = serializers.CharField(source='get_form_item_type_display', read_only=True)
    rule = serializers.JSONField(allow_null=True,required=False)
    data_options = serializers.JSONField(allow_null=True,required=False)
    setting = serializers.JSONField(allow_null=True,required=False)

    class Meta:
        model = SystemConfig
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {
            'key': {'required': False},
            'title': {'required': False},
        }

    def validate_key(self, value):
        """
        验证key是否允许重复
        parent为空时不允许重复,反之允许
        """
        ins = getattr(self, 'instance', None)
        instance = SystemConfig.objects.exclude(id=ins.id).filter(key=value, parent__isnull=True).exists()
        if instance:
            raise ValueError('已存在相同变量名')
        return value

class SystemConfigViewSet(CustomModelViewSet):
    """
    系统配置接口
    """
    queryset = SystemConfig.objects.order_by('sort', 'create_datetime')
    serializer_class = SystemConfigChildrenSerializer
    create_serializer_class = SystemConfigCreateSerializer
    update_serializer_class = SystemConfigUpdateSerializer
    filter_class = SystemConfigFilter

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        body = request.data
        serializer = self.get_serializer(instance, data=body, request=request, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return DetailResponse(data=serializer.data, msg="更新成功")

    def save_content(self, request,pk):
        body = request.data
        data_mapping = {item['id']: item for item in body}
        for obj_id, data in data_mapping.items():
            instance_obj = SystemConfig.objects.filter(id=obj_id).first()
            if instance_obj is None:
                serializer = SystemConfigCreateSerializer(data=data)
            else:
                serializer = SystemConfigCreateSerializer(instance_obj, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        return DetailResponse(msg="保存成功")

    def get_models_info_list(self, request):
        """
        获取所有的model及字段信息
        """
        res = [e.get('table') for e in get_all_models_objects().values()]
        return DetailResponse(msg="获取成功", data=res)

# ================================================= #
# ************** 前端用户获取平台配置信息 view  ************** #
# ================================================= #

def getSystemConfig(key="base",group = True):
    """
    当group=False时，表示查询具体的一个key的信息，这里的key用 base.logo 即 父key.子key 的方式访问
    当group=True时，表示查询一个parent 为指定key的组信息
    """
    if group:
        queryset = SystemConfig.objects.filter(parent__key=key).values('value','key','form_item_type')
    else:
        keys = key.split('.')  # 拆分成 ["a", "b"]
        if len(keys) == 2:
            queryset = SystemConfig.objects.filter(parent__key=keys[0],key=keys[1]).values('value','key','form_item_type')
        elif len(keys) == 1:
            queryset = SystemConfig.objects.filter(key=key).values('value','key','form_item_type')
        else:
            raise Exception("key格式错误")
    data = {}
    if queryset:
        for m in queryset:
            if m['form_item_type']  == 9:
                m['value'] = boolValue(m['value'])
            data[m['key']] = m['value']
    return data

class GetSystemConfigSettingsView(APIView):
    """
    get:
    获取系统配置
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = getSystemConfig()
        return DetailResponse(data=data)