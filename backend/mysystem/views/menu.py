# -*- coding: utf-8 -*-

"""
@Remark: 菜单模块
"""
from rest_framework import serializers

from mysystem.models import Menu, MenuButton, Button
from mysystem.views.menu_button import MenuButtonSerializer
from utils.jsonResponse import SuccessResponse,DetailResponse,ErrorResponse
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet
from utils.common import get_parameter_dic,ast_convert
from django.db.models import Q
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated


class MenuSerializer(CustomModelSerializer):
    """
    菜单表的简单序列化器
    """

    class Meta:
        model = Menu
        fields = "__all__"
        # exclude = ('description', 'creator', 'modifier')
        read_only_fields = ["id"]


class MenuCreateSerializer(CustomModelSerializer):
    """
    菜单表的创建序列化器
    """
    name = serializers.CharField(required=False)

    class Meta:
        model = Menu
        fields = "__all__"
        #exclude = ('description', 'creator', 'modifier')
        read_only_fields = ["id"]


class MenuTreeSerializer(CustomModelSerializer):
    """
    菜单表的树形序列化器
    """
    children = serializers.SerializerMethodField(read_only=True)
    menuPermission_name = serializers.SerializerMethodField(read_only=True)
    menuPermission = MenuButtonSerializer(read_only=True,many=True)

    def get_children(self, instance):
        queryset = Menu.objects.filter(parent=instance.id).filter(status=1)
        if queryset:
            serializer = MenuTreeSerializer(queryset, many=True)
            return serializer.data
        else:
            return None

    def get_menuPermission_name(self, instance):
        queryset = MenuButton.objects.filter(menu=instance.id).values_list('name', flat=True)
        if queryset:
            return queryset
        else:
            return None

    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ["id"]


class WebRouterSerializer(CustomModelSerializer):
    """
    前端菜单路由的简单序列化器
    """

    class Meta:
        model = Menu
        fields = ('id', 'parent', 'icon', 'sort', 'web_path', 'name', 'type','link_url', 'component','component_name', 'cache', 'visible', 'status')
        read_only_fields = ["id"]

class MenuViewSet(CustomModelViewSet):
    """
    菜单管理接口
    list:查询
    create:新增
    update:修改
    retrieve:详情
    destroy:删除
    """
    queryset = Menu.objects.all().order_by('sort')
    serializer_class = MenuSerializer
    create_serializer_class = MenuCreateSerializer
    update_serializer_class = MenuCreateSerializer
    filterset_fields = ['name', 'status','visible']
    search_fields = ['name','web_path']

    def update_sort(self,request):
        """菜单排序（上移、下移、拖拽）"""
        reqData = get_parameter_dic(request)
        menu_list = ast_convert(reqData.get("menus", []))
        if not menu_list:return ErrorResponse(msg="没有提供数据")
        menu_ids = [item['id'] for item in menu_list]
        if not menu_ids:return ErrorResponse(msg="参数错误")
        menus = Menu.objects.filter(id__in=menu_ids)
        menu_dict = {menu.id: menu for menu in menus}

        # 更新 sort 字段
        updated_menus = []
        for item in menu_list:
            menu_id = item['id']
            sort_value = item['sort']
            parent_value = item['parent'] if item['parent'] else None
            if menu_id in menu_dict:
                menu_dict[menu_id].sort = sort_value
                menu_dict[menu_id].parent_id = parent_value
                updated_menus.append(menu_dict[menu_id])

        if not updated_menus:
            return ErrorResponse(msg="无此菜单") 

        Menu.objects.bulk_update(updated_menus, ['sort','parent_id'])

        return DetailResponse(msg="操作成功")

    def menu_tree(self, request):
        """用于菜单添加修改中获取父级菜单"""
        queryset = Menu.objects.filter(parent=None)
        serializer = MenuTreeSerializer(queryset, many=True)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    # @action(methods=['get'],extra_filter_backends=[],detail=False)#会自动生成/api/system/menu/web_router/的路由
    def web_router(self, request):
        """用于前端获取当前角色的路由"""
        user = request.user
        if user.is_superuser:
            queryset = self.queryset.filter(status=True).order_by("sort")
        else:
            menuIds = user.role.values_list('menu__id', flat=True)
            queryset = self.filter_queryset(Menu.objects.filter(id__in=menuIds, status=True))
        serializer = WebRouterSerializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")
