#!/bin/python
#coding: utf-8
# +-------------------------------------------------------------------
# | system: dvlyadmin-mini
# +-------------------------------------------------------------------
# | Author: lybbn
# +-------------------------------------------------------------------
# | QQ: 1042594286
# +-------------------------------------------------------------------

# ------------------------------
# 获取初始化数据
# ------------------------------
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import models

class Command(BaseCommand):
    help = '快速获取指定模型的字段数据,用法：python manage.py get_init_data your_app.models_name'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='模型名称（格式：app_label.ModelName）')
        parser.add_argument(
            '--fields', 
            type=str, 
            help='指定要获取的字段（逗号分隔），未指定则获取全部字段（除EXCLUDE_FIELDS之外的所有字段）'
        )
        parser.add_argument(
            '--exclude',
            type=str,
            help='要排除的字段（逗号分隔），会覆盖默认排除字段'
        )
        parser.add_argument(
            '--order_by', 
            type=str, 
            default='id',
            help='排序字段（默认：id）'
        )

    def handle(self, *args, **options):
        model_name = options['model_name']
        fields = options.get('fields', '').split(',') if options.get('fields') else None
        order_by = options['order_by']

        EXCLUDE_FIELDS = ['create_datetime', 'update_datetime', 'is_delete','modifier','dept_belong']  # 根据您的实际情况调整
        try:
            # 获取模型类
            model = apps.get_model(model_name)
            
            # 验证是否是Django模型
            if not issubclass(model, models.Model):
                self.stderr.write(self.style.ERROR(f'{model_name} 不是有效的Django模型'))
                return

            # 获取所有字段或指定字段
            if not fields:
                # # 获取所有非关系字段
                # fields = [f.name for f in model._meta.fields if not f.is_relation]
                # 获取除指定EXCLUDE_FIELDS之外的字段
                fields = [
                    f.name for f in model._meta.fields if f.name not in EXCLUDE_FIELDS
                ]
            
            # 查询数据
            queryset = model.objects.all().order_by(order_by)
            
            # 输出数据
            result = []
            for obj in queryset:
                item = {}
                for field in fields:
                    try:
                        field_obj = model._meta.get_field(field)
                        value = getattr(obj, field)
                        
                        # 处理外键关系（只获取ID）
                        if isinstance(field_obj, models.ForeignKey):
                            item[f"{field}_id"] = value.id if value else None
                        else:
                            item[field] = value
                    except Exception as e:
                        item[field] = f"ERROR: {str(e)}"
                result.append(item)

            # 输出结果
            self.stdout.write(self.style.SUCCESS(f"\n{options['model_name']} 数据（共 {len(result)} 条）："))
            for item in result:
                self.stdout.write(str(item)+',')
            
        except LookupError:
            self.stderr.write(self.style.ERROR(f'找不到模型: {model_name}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'发生错误: {str(e)}'))