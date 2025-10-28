"""
URL configuration for application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include, re_path
from django.views.static import serve
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularJSONAPIView, SpectacularRedocView, SpectacularSwaggerView
from utils.permission import CustomPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

#自定义
from utils.streamingmedia_response import streamingmedia_serve
from mysystem.views.login import LoginView,CaptchaView
from mysystem.views.frontend import h5web

urlpatterns = [
    path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT},),  # 处理静态文件
    path('media/<path:path>', streamingmedia_serve, {'document_root': settings.MEDIA_ROOT}, ),  # 处理媒体文件
    
    #接口文档（线上部署需注释掉，确保安全性，已添加需认证访问增强安全性）
    path('api/schema/lyjson/', SpectacularJSONAPIView.as_view(authentication_classes=[JWTAuthentication],permission_classes=[IsAuthenticated,CustomPermission]), name='schema-auth'),
]

if settings.DEBUG:
    #接口文档（线上部署需注释掉，确保安全性）
    urlpatterns += [
        path('api/schema/lyjson-public/', SpectacularJSONAPIView.as_view(), name='schema'),
        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]

urlpatterns += [
    #管理后台的标准接口
    path('api/system/', include('mysystem.urls')),
    path('api/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/captcha/', CaptchaView.as_view()),
]

urlpatterns += [
    #集成部署后端管理页面和uniapp h5页面
    path('h5/',h5web ,name='h5端页面部署'),
    path('favicon.ico',RedirectView.as_view(url=r'static/favicon.ico')),
    path('', TemplateView.as_view(template_name="lyadmin/index.html"),name='后台管理默认页面'),
]