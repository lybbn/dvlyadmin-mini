---
name: "dvlyadmin-json-response"
description: "指导如何在项目中正确使用 SuccessResponse、DetailResponse、ErrorResponse 响应类。当编写 Django REST API 视图返回数据时，必须调用此 skill 获取正确的响应方式。"
---

# Django API 响应类使用指南

## 响应类位置
`backend/utils/jsonResponse.py`

## 三种响应类概述

| 响应类 | 用途 | 返回格式 |
|--------|------|----------|
| `SuccessResponse` | 分页列表数据 | 包含 page、limit、total、data |
| `DetailResponse` | 单条数据或非分页数据 | 直接返回 data |
| `ErrorResponse` | 错误信息 | 包含 code、msg、data |

## 何时使用

### SuccessResponse - 分页列表场景
- 列表查询接口（有分页）
- 需要返回总数、页码等信息
- 后台管理系统的列表页面

### DetailResponse - 单条数据场景
- 获取详情接口
- 创建/更新成功后返回数据
- 不需要分页的数据列表
- 操作成功提示（无返回数据）

### ErrorResponse - 错误场景
- 参数验证失败
- 权限不足
- 业务逻辑错误
- 资源不存在

## 导入方式

```python
from utils.jsonResponse import SuccessResponse, DetailResponse, ErrorResponse
```

## SuccessResponse 使用详解

### 返回格式
```json
{
    "code": 2000,
    "data": {
        "page": 1,
        "limit": 20,
        "total": 100,
        "data": [...]
    },
    "msg": "success"
}
```

### 基本用法
```python
def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return SuccessResponse(
            data=serializer.data,
            page=request.query_params.get('page', 1),
            limit=request.query_params.get('limit', 20),
            total=queryset.count()
        )
    serializer = self.get_serializer(queryset, many=True)
    return SuccessResponse(data=serializer.data)
```

### 完整示例
```python
class MyViewSet(CustomModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MySerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 20))
        
        total = queryset.count()
        queryset = queryset[(page - 1) * limit:page * limit]
        
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(
            data=serializer.data,
            page=page,
            limit=limit,
            total=total
        )
```

### 自定义消息
```python
return SuccessResponse(
    data=serializer.data,
    page=page,
    limit=limit,
    total=total,
    msg="查询成功"
)
```

## DetailResponse 使用详解

### 返回格式
```json
{
    "code": 2000,
    "data": {...},
    "msg": "success"
}
```

### 场景1：获取详情
```python
def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return DetailResponse(data=serializer.data)
```

### 场景2：创建成功
```python
def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return DetailResponse(data=serializer.data, msg="创建成功")
```

### 场景3：更新成功
```python
def update(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return DetailResponse(data=serializer.data, msg="更新成功")
```

### 场景4：操作成功无返回数据
```python
@action(detail=True, methods=['post'])
def enable(self, request, pk=None):
    instance = self.get_object()
    instance.status = True
    instance.save()
    return DetailResponse(msg="启用成功")
```

### 场景5：非分页列表
```python
@action(detail=False, methods=['get'])
def options(self, request):
    """获取下拉选项列表"""
    queryset = self.get_queryset().filter(status=True)
    serializer = self.get_serializer(queryset, many=True)
    return DetailResponse(data=serializer.data)
```

## ErrorResponse 使用详解

### 返回格式
```json
{
    "code": 400,
    "data": null,
    "msg": "error"
}
```

### 常用错误码

| 错误码 | 含义 | 使用场景 |
|--------|------|----------|
| 400 | 参数错误 | 请求参数验证失败 |
| 401 | 未授权 | 未登录或token无效 |
| 403 | 禁止访问 | 无权限访问 |
| 404 | 未找到 | 资源不存在 |
| 429 | 请求过多 | 频率限制 |
| 500 | 服务器错误 | 内部错误 |
| 503 | 服务不可用 | 服务暂停 |

### 场景1：参数错误
```python
def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if not serializer.is_valid():
        return ErrorResponse(
            msg="参数验证失败",
            data=serializer.errors,
            code=400
        )
    serializer.save()
    return DetailResponse(data=serializer.data)
```

### 场景2：权限错误
```python
def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    if instance.creator_id != request.user.id and not request.user.is_superuser:
        return ErrorResponse(msg="无权限删除此数据", code=403)
    instance.delete()
    return DetailResponse(msg="删除成功")
```

### 场景3：资源不存在
```python
def get_object(self):
    try:
        return super().get_object()
    except Http404:
        raise Http404
```

### 场景4：业务逻辑错误
```python
@action(detail=True, methods=['post'])
def publish(self, request, pk=None):
    instance = self.get_object()
    if instance.status == 'published':
        return ErrorResponse(msg="该内容已发布", code=400)
    instance.status = 'published'
    instance.save()
    return DetailResponse(msg="发布成功")
```

### 场景5：余额不足
```python
def check_balance(user):
    balance = UserBalance.objects.get(user=user)
    if balance.balance <= 0:
        return ErrorResponse(msg="余额不足，请先充值", code=402)
    return None
```

## 完整视图示例

```python
from utils.jsonResponse import SuccessResponse, DetailResponse, ErrorResponse

class ArticleViewSet(CustomModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def list(self, request, *args, **kwargs):
        """列表查询 - 使用 SuccessResponse"""
        queryset = self.filter_queryset(self.get_queryset())
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 20))
        
        total = queryset.count()
        queryset = queryset[(page - 1) * limit:page * limit]
        
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(
            data=serializer.data,
            page=page,
            limit=limit,
            total=total
        )
    
    def retrieve(self, request, *args, **kwargs):
        """详情查询 - 使用 DetailResponse"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return DetailResponse(data=serializer.data)
    
    def create(self, request, *args, **kwargs):
        """创建 - 使用 DetailResponse"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ErrorResponse(msg="参数错误", data=serializer.errors, code=400)
        serializer.save(creator=request.user)
        return DetailResponse(data=serializer.data, msg="创建成功")
    
    def update(self, request, *args, **kwargs):
        """更新 - 使用 DetailResponse"""
        instance = self.get_object()
        if instance.creator != request.user and not request.user.is_superuser:
            return ErrorResponse(msg="无权限修改", code=403)
        
        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            return ErrorResponse(msg="参数错误", data=serializer.errors, code=400)
        serializer.save()
        return DetailResponse(data=serializer.data, msg="更新成功")
    
    def destroy(self, request, *args, **kwargs):
        """删除 - 使用 DetailResponse"""
        instance = self.get_object()
        if instance.creator != request.user and not request.user.is_superuser:
            return ErrorResponse(msg="无权限删除", code=403)
        instance.delete()
        return DetailResponse(msg="删除成功")
    
    @action(detail=False, methods=['get'])
    def options(self, request):
        """下拉选项 - 使用 DetailResponse（非分页列表）"""
        queryset = self.get_queryset().filter(status=True)
        serializer = self.get_serializer(queryset, many=True)
        return DetailResponse(data=serializer.data)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """发布操作 - 使用 DetailResponse 或 ErrorResponse"""
        instance = self.get_object()
        
        if instance.is_published:
            return ErrorResponse(msg="已发布，请勿重复操作", code=400)
        
        instance.is_published = True
        instance.save()
        return DetailResponse(msg="发布成功")
```

## 注意事项

1. **SuccessResponse 默认 code 为 2000**，不支持自定义其他 code
2. **DetailResponse 默认 code 为 2000**，不支持自定义其他 code
3. **ErrorResponse 默认 code 为 400**，可以自定义 code
4. **前端判断成功条件**：`res.code === 2000`
5. **分页数据必须使用 SuccessResponse**，确保前端分页组件正常工作
6. **错误响应的 data 字段**可以返回错误详情，如验证错误信息
