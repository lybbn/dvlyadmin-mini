# -*- coding: utf-8 -*-

"""
@Remark: websocket的路由文件
"""
from django.urls import re_path,path

from mysystem.views.wsmessage import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'^ws/msg/$', NotificationConsumer.as_asgi()),
]