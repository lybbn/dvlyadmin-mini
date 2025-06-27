# -*- coding: utf-8 -*-

"""
@Remark: 系统管理的路由文件
"""
from django.urls import path, re_path
from rest_framework import routers

from mysystem.views.button import ButtonViewSet
from mysystem.views.dept import DeptViewSet
from mysystem.views.menu import MenuViewSet
from mysystem.views.menu_button import MenuButtonViewSet
from mysystem.views.operation_log import OperationLogViewSet
from mysystem.views.role import RoleViewSet,RolePermissionViewSet
from mysystem.views.user import UserViewSet
from mysystem.views.menu_field import MenuFieldViewSet

system_url = routers.SimpleRouter()
system_url.register(r'menu', MenuViewSet)
system_url.register(r'button', ButtonViewSet)
system_url.register(r'menu_button', MenuButtonViewSet)
system_url.register(r'menu_field', MenuFieldViewSet)
system_url.register(r'role', RoleViewSet)
system_url.register(r'role_permission', RolePermissionViewSet,basename="role_permission")
system_url.register(r'dept', DeptViewSet)
system_url.register(r'user', UserViewSet)
system_url.register(r'operation_log', OperationLogViewSet)

urlpatterns = [
    re_path('menu/update_sort/', MenuViewSet.as_view({'post': 'update_sort'})),
    re_path('menu_tree/', MenuViewSet.as_view({'get': 'menu_tree'})),
    
    re_path('menu_button/menu_button_permission/', MenuButtonViewSet.as_view({'get': 'menu_button_permission'})),
    re_path('menu_button/batch_generate/', MenuButtonViewSet.as_view({'post': 'batch_generate'})),

    re_path('menu_field/get_models/', MenuFieldViewSet.as_view({'get': 'get_models'})),
    re_path('menu_field/auto_create/', MenuFieldViewSet.as_view({'post': 'auto_create'})),
    re_path('menu/web_router/', MenuViewSet.as_view({'get': 'web_router'})),#也可以在视图的action装饰器中自动生成
    
    re_path('dept/set_status/', DeptViewSet.as_view({'post': 'set_status'})),
    re_path('role/set_status/', RoleViewSet.as_view({'post': 'set_status'})),

    re_path('role_id_to_menu/(?P<pk>.*?)/', RoleViewSet.as_view({'get': 'roleId_to_menu'})),
    re_path('role_permission/save_permission/', RolePermissionViewSet.as_view({'post': 'save_permission'})),
    
    
    re_path('operation_log/deletealllogs/',OperationLogViewSet.as_view({'delete':'deletealllogs'})),

    path('user/user_info/',UserViewSet.as_view({'get':'user_info','put':'update_user_info'})),
    re_path('user/change_password/(?P<pk>.*?)/',UserViewSet.as_view({'put':'change_password'})),
]
urlpatterns += system_url.urls
