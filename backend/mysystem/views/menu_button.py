# -*- coding: utf-8 -*-

"""
@Remark: 菜单按钮管理
"""
from mysystem.models import MenuButton,Menu
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet
from utils.common import get_parameter_dic
from utils.jsonResponse import SuccessResponse,DetailResponse,ErrorResponse


class MenuButtonSerializer(CustomModelSerializer):
    """
    菜单按钮-序列化器
    """

    class Meta:
        model = MenuButton
        fields = "__all__"
        read_only_fields = ["id"]


class MenuButtonViewSet(CustomModelViewSet):
    """
    菜单按钮接口:
    """
    queryset = MenuButton.objects.all()
    serializer_class = MenuButtonSerializer
    filterset_fields = ['menu']

    def batch_generate(self,request):
        """自动批量生成增删改查详情 按钮权限"""
        reqData = get_parameter_dic(request)
        menu_id = reqData.get("menu", "")
        baseapi = reqData.get("baseapi", "")#若不提供基础api前缀，则默认为组件名
        if not menu_id:return ErrorResponse(msg="请提供要添加的菜单")
        ins = Menu.objects.filter(id=menu_id).first()
        if not ins:return ErrorResponse(msg="无此菜单")
        if not baseapi:
            baseapi = f'/api/{ins.component_name}/'
        data_list = [
            {'menu': ins.id, 'name': '新增', 'value': f'{ins.component_name}:Create', 'api': f'{baseapi}', 'method': 1},
            {'menu': ins.id, 'name': '删除', 'value': f'{ins.component_name}:Delete', 'api': f'{baseapi}{{id}}/', 'method': 3},
            {'menu': ins.id, 'name': '编辑', 'value': f'{ins.component_name}:Update', 'api': f'{baseapi}{{id}}/', 'method': 2},
            {'menu': ins.id, 'name': '查询', 'value': f'{ins.component_name}:Search', 'api': f'{baseapi}', 'method': 0},
            {'menu': ins.id, 'name': '详情', 'value': f'{ins.component_name}:Detail', 'api': f'{baseapi}{{id}}/', 'method': 0},
        ]
        serializer = self.get_serializer(data=data_list, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return DetailResponse(msg="批量生成成功")
