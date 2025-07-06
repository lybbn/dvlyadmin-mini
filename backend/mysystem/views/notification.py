# -*- coding: utf-8 -*-

"""
@Remark: 消息通知
"""
import django_filters
from mysystem.models import Notification,NotificationUsers
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet
from utils.common import get_parameter_dic
from utils.jsonResponse import SuccessResponse,DetailResponse,ErrorResponse

class NotificationFilterSet(django_filters.rest_framework.FilterSet):
    """
    消息通知 过滤器
    """
    #开始时间
    beginAt = django_filters.DateTimeFilter(field_name='create_datetime', lookup_expr='gte')  # 指定过滤的字段
    #结束时间
    endAt = django_filters.DateTimeFilter(field_name='create_datetime', lookup_expr='lte')
    title = django_filters.CharFilter(field_name='title',lookup_expr='icontains')

    class Meta:
        model = Notification
        fields = ['beginAt', 'endAt', 'title']

class NotificationSerializer(CustomModelSerializer):
    """
    消息通知-序列化器
    """

    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ["id"]


class NotificationViewSet(CustomModelViewSet):
    """
    消息通知接口:
    """
    queryset = Notification.objects.all().order_by("-create_datetime")
    serializer_class = NotificationSerializer