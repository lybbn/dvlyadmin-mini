# -*- coding: utf-8 -*-

"""
@Remark: 消息通知
"""
import datetime
import django_filters
from mysystem.models import Notification,NotificationUsers,Users
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet
from utils.common import get_parameter_dic
from utils.jsonResponse import SuccessResponse,DetailResponse,ErrorResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import serializers
from django.db import transaction
from django.db.models import Q

def websocket_push(user_id, message):
    """
    主动推送消息
    """
    room_group_name = "notifications_user_" + str(user_id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            "type": "push.message",
            "json": message
        }
    )

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

class NotificationUsersFilterSet(django_filters.rest_framework.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    is_read = django_filters.BooleanFilter(field_name='is_read')
    
    class Meta:
        model = NotificationUsers
        fields = ['is_read']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(notification__title__icontains=value) |
            Q(notification__content__icontains=value)
        )

class NotificationSerializer(CustomModelSerializer):
    """
    消息通知-序列化器
    """

    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ["id"]

class NotificationUsersSerializer(CustomModelSerializer):
    """
    消息通知 用户-序列化器
    """

    class Meta:
        model = NotificationUsers
        fields = "__all__"
        read_only_fields = ["id"]

class NotificationCreateUpdateSerializer(CustomModelSerializer):
    """
    消息通知 - 创建\编辑 序列化器
    """
    @transaction.atomic()
    def save(self, **kwargs):
        data = super().save(**kwargs)
        initial_data = self.initial_data
        target_type = initial_data.get('target_type')
        
        # 获取现有关联用户ID集合（如果是更新操作）
        existing_user_ids = set()
        if self.instance and self.instance.pk:
            existing_user_ids = set(NotificationUsers.objects.filter(
                notification=self.instance
            ).values_list('user_id', flat=True))
        
        # 根据目标类型确定目标用户
        if target_type in [0]:  # 平台公告
            users = Users.objects.filter(is_delete=False).values_list('id', flat=True)
        elif target_type in [1]:  # 按用户
            users = initial_data.get('users', [])
        
        # 转换为集合便于操作
        new_user_ids = set(users)
        
        # 需要删除的关联（存在于现有但不在新列表中）
        to_delete_ids = existing_user_ids - new_user_ids
        if to_delete_ids:
            NotificationUsers.objects.filter(
                notification=data,
                user_id__in=to_delete_ids
            ).delete()
        
        # 需要新增的关联（存在于新列表但不在现有中）
        to_create_ids = new_user_ids - existing_user_ids
        targetuser_data = []
        for user_id in to_create_ids:
            targetuser_data.append({
                "notification": data.id,
                "user": user_id
            })
        
        if targetuser_data:
            targetuser_instance = NotificationUsersSerializer(
                data=targetuser_data, 
                many=True, 
                request=self.request
            )
            targetuser_instance.is_valid(raise_exception=True)
            targetuser_instance.save()
        
        # 发送WebSocket通知
        for user_id in new_user_ids:
            unread_nums = NotificationUsers.objects.filter(
                user_id=user_id, 
                is_read=False
            ).count()
            websocket_push(
                user_id, 
                message={
                    "sender": 'system', 
                    "msg_type": 'SYS',
                    "content": '您有一条新消息~', 
                    "unread": unread_nums
                }
            )
        
        return data

    class Meta:
        model = Notification
        read_only_fields = ["id"]
        fields = '__all__'
        # exclude = ['password']

class NotificationListSerializer(CustomModelSerializer):
    """
    用户消息列表序列化器-序列化器
    """

    class Meta:
        model = Notification
        fields = ("id","target_type","tag_type","title","content","create_datetime")
        read_only_fields = ["id"]

class NotificationUsersListSerializer(CustomModelSerializer):
    """
    目标用户序列化器-序列化器
    """
    notification = NotificationListSerializer()

    class Meta:
        model = NotificationUsers
        fields = "__all__"
        read_only_fields = ["id"]

class NotificationViewSet(CustomModelViewSet):
    """
    消息通知接口:
    """
    queryset = Notification.objects.all().order_by("-create_datetime")
    serializer_class = NotificationSerializer
    filterset_class = NotificationFilterSet
    create_serializer_class = NotificationCreateUpdateSerializer
    update_serializer_class = NotificationCreateUpdateSerializer
    search_fields = ('title',)

    def get_own_receive(self, request):
        """
        获取自己的接收消息
        """
        user = self.request.user
        queryset = NotificationUsers.objects.filter(user=user,is_delete=False).order_by("-id")
        filterset = NotificationUsersFilterSet(request.query_params, queryset=queryset)
        queryset = filterset.qs
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = NotificationUsersListSerializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = NotificationUsersListSerializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")
    
    def del_own_receive(self, request):
        """
        删除自己的接收消息
        """
        reqData = get_parameter_dic(request)
        id = reqData.get("id")
        user = self.request.user
        NotificationUsers.objects.filter(id=id,user=user).update(is_delete=True)
        return SuccessResponse(msg="删除成功")
    
    def read_own_receive(self, request):
        """
        设置自己的接收消息已读
        """
        reqData = get_parameter_dic(request)
        id = reqData.get("id")
        user = self.request.user
        NotificationUsers.objects.filter(id=id,user=user,is_read=False).update(is_read=True,read_at=datetime.datetime.now())
        return SuccessResponse(msg="删除成功")