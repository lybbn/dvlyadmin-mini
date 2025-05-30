# -*- coding: utf-8 -*-

"""
@Remark: 菜单列管理
"""
from utils.models import get_project_app_models
from mysystem.models import MenuField,Menu
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet
from utils.common import get_parameter_dic
from utils.jsonResponse import SuccessResponse,DetailResponse,ErrorResponse

class MenuFieldSerializer(CustomModelSerializer):
    """
    菜单列-序列化器
    """

    class Meta:
        model = MenuField
        fields = "__all__"
        read_only_fields = ["id"]


class MenuFieldViewSet(CustomModelViewSet):
    """
    菜单列接口:
    """
    queryset = MenuField.objects.all()
    serializer_class = MenuFieldSerializer
    filterset_fields = ['menu']

    def get_models(self, request):
        """获取所有自定义项目app下的model"""
        data = []
        for model in get_project_app_models(include_fields=False):
            data.append({
                'app': model['app'],
                'title': model['verbose'],
                'model': model['model']
            })
        return DetailResponse(data=data)

    def auto_create(self,request):
        """自动批量生成列"""
        reqData = get_parameter_dic(request)
        menu_id = reqData.get("menu", "")
        model_name = reqData.get("model", "")#若不提供指定model，则默认为自动发现该菜单模型名
        if not menu_id:return ErrorResponse(msg="请提供要添加的菜单")
        if not model_name:return ErrorResponse(msg="请提供所属模型名")
        ins = Menu.objects.filter(id=menu_id).first()
        if not ins:return ErrorResponse(msg="无此菜单")
        for model in get_project_app_models():
            if model['model'] == model_name:
                for field in model['fields']:
                    if MenuField.objects.filter(menu_id=menu_id, model=model_name, field_name=field['name']).exists():
                        continue
                    data = {
                        'menu': menu_id,
                        'model': model_name,
                        'field_name': field['name'],
                        'title': str(field['title']),
                    }
                    serializer = self.get_serializer(data=data, request=request)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
        return DetailResponse(msg="生成成功")
