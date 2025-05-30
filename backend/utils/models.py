# -*- coding: utf-8 -*-

"""
@Remark: 公共基础model类
"""
import uuid

from django.apps import apps

from django.db import models

from application import settings

from importlib import import_module

table_prefix = "lyadmin_"  # 数据库表名前缀


def make_uuid():
    # .hex 将生成的uuid字符串中的 － 删除，带-是36位字符，不带-是32位随机字符串
    return str(uuid.uuid4().hex)

class CoreModel(models.Model):
    """
    核心标准抽象模型模型,可直接继承使用
    增加审计字段, 覆盖字段时, 字段名称请勿修改, 必须统一审计字段名称
    """
    # id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    id = models.CharField(max_length=100, primary_key=True, default=make_uuid, help_text="Id", verbose_name="Id")
    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_query_name='creator_query', null=True,verbose_name='创建人', help_text="创建人", on_delete=models.SET_NULL, db_constraint=False)
    modifier = models.CharField(max_length=100, null=True, blank=True, help_text="修改人", verbose_name="修改人")
    dept_belong = models.CharField(max_length=100, help_text="数据归属部门", null=True, blank=True, verbose_name="数据归属部门")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",verbose_name="创建时间")

    class Meta:
        abstract = True
        verbose_name = '核心模型'
        verbose_name_plural = verbose_name

class BaseModel(models.Model):
    """
    基本模型,可直接继承使用，一般不需要使用审计字段的模型可以使用
    覆盖字段时, 字段名称请勿修改
    """
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='更新时间')
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    is_delete = models.BooleanField(default=False, verbose_name="是否逻辑删除", help_text="是否逻辑删除")

    class Meta:
        abstract = True  # 表示该类是一个抽象类，只用来继承，不参与迁移操作
        verbose_name = '基本模型'
        verbose_name_plural = verbose_name

def get_all_models_objects(model_name= None,exclude_modules= None,include_fields = True):
    """
    获取所有模型对象信息（带缓存和灵活过滤）
    
    Args:
        model_name: 指定模型名时返回单个模型，否则返回全部
        exclude_modules: 自定义排除的模块路径（覆盖默认配置）
        include_fields: 是否包含字段信息（大型模型可关闭提升性能）
    
    Returns:
        Dict: {
            "ModelName": {
                "table": {
                    "table_name": "verbose_name",
                    "db_table": "db_table_name",
                    "class_name": "ModelName",
                    "tableFields": [{"name": "field1", "type": "CharField",title:"verbose_name"}, ...],
                    "import_path": "from app.models import ModelName"
                },
                "object": <ModelClass>
            }
        }
    """
    # 默认排除的模块（可被参数覆盖）
    DEFAULT_EXCLUDE_MODULES = [
        'django.contrib.admin.models',
        'django.contrib.sessions.models',
        'django.contrib.auth.models',
        'django.contrib.contenttypes.models',
        'captcha.models',
        'django_celery_results.models',
        'django_celery_beat.models'
    ]
    
    # 使用缓存避免重复查询
    if not hasattr(settings, 'ALL_MODELS_OBJECTS'):
        settings.ALL_MODELS_OBJECTS = {}
    
    # 仅当缓存为空时重新加载
    if not settings.ALL_MODELS_OBJECTS:
        exclude_modules = exclude_modules or DEFAULT_EXCLUDE_MODULES
        all_models = apps.get_models()
        
        for model in all_models:
            module_path = model.__module__
            
            if any(module_path.startswith(excluded) for excluded in exclude_modules):
                continue
                
            model_info = {
                "table_name": model._meta.verbose_name,
                "db_table": model._meta.db_table,
                "class_name": model.__name__,
                "import_path": f"from {module_path} import {model.__name__}",
                "tableFields": []
            }
            
            if include_fields:
                for field in model._meta.fields:
                    fields = {"title": getattr(field, 'verbose_name', ''), "name": field.name,"type":field.get_internal_type()}
                    model_info['tableFields'].append(fields)
            
            settings.ALL_MODELS_OBJECTS[model.__name__] = {
                "table": model_info,
                "object": model
            }
    
    # 返回指定模型或全部
    if model_name:
        return settings.ALL_MODELS_OBJECTS.get(model_name, {})
    return settings.ALL_MODELS_OBJECTS.copy()  # 返回副本防止外部修改

def get_model_info_by_app(app_name,include_fields = True):
    """
    获取指定app下的所有模型及其字段信息
    
    Args:
        app_name: Django应用名（如'mysystem'）
        include_fields: 是否包含字段信息（大型模型可关闭提升性能）
    
    Returns:
        List[Dict]: 模型信息列表，每个模型包含：
            - app: 应用名
            - verbose: 模型verbose_name
            - model: 模型类名
            - object: 模型类
            - fields: 字段列表（包含verbose_name, name, field_object）
    
    Raises:
        ImportError: 当models.py不存在时
    """
    try:
        model_module = import_module(f'{app_name}.models')
    except ImportError as e:
        return []

    exclude_models = getattr(model_module, 'exclude_models', [])
    
    # 使用更精确的模型过滤
    model_classes = [
        cls for cls in model_module.__dict__.values()
        if isinstance(cls, type) 
        and issubclass(cls, models.Model)
        and cls.__name__ not in exclude_models
        and cls.__name__ != 'CoreModel'
        and not cls._meta.abstract  # 排除抽象模型
    ]

    result = []
    for model in model_classes:
        fields = []
        if include_fields:
            fields = [
                {
                    'title': getattr(field, 'verbose_name', ''),
                    'name': field.name,
                    'type': field.get_internal_type(),
                    'object': field
                }
                for field in model._meta.fields
                if hasattr(field, 'name')  # 基础字段（排除反向关联字段等）
            ]
            
        result.append({
            'app': app_name,
            'verbose': model._meta.verbose_name,
            'model': model.__name__,
            'object': model,
            'fields': fields
        })
    
    return result

def get_project_app_models(app_name = None,exclude_apps= None,include_fields = True):
    """
    获取项目用户所有自定义app的模型（排除django内置app和三方django依赖app）
    
    Args:
        app_name: 可选，指定单个app时只返回该app的模型
        exclude_apps: 自定义排除的模块名（覆盖默认配置）
        include_fields: 是否包含字段信息（大型模型可关闭提升性能）
    
    Returns:
        List[Dict]: 同get_model_info_by_app返回值
    """
    if app_name:
        return get_model_info_by_app(app_name,include_fields = include_fields)
    
    result = []
    DEFAULT_EXCLUDE_APPS = [
        'corsheaders',
        'rest_framework',
        'channels',
        'captcha',
        'drf_spectacular',
        'drf_spectacular_sidecar'
    ]
    exclude_apps = exclude_apps or DEFAULT_EXCLUDE_APPS
    for app_config in apps.get_app_configs():
        if (
            app_config.name.startswith('django') or
            app_config.name in exclude_apps
        ):
            continue
        
        try:
            models = get_model_info_by_app(app_config.name,include_fields = include_fields)
            result.extend(models)
        except Exception as e:
            pass
    
    return result

def is_table_exists(table_name):
    """
    检查表名是否存在
    """
    from django.db import connection
    return table_name in connection.introspection.table_names()