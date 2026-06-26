---
name: "dvlyadmin-initialize-data"
description: "指导如何在 dvlyadmin-mini 项目中通过 initialize.py 添加初始化数据。Invoke when user wants to add seed/init data to database or create new init methods."
---

# dvlyadmin-mini 初始化数据添加指南

## 核心文件

- **初始化类**: `backend/mysystem/initialize.py` — `Initialize` 类 + `main()` 入口函数
- **初始化命令**: `backend/mysystem/management/commands/init.py` — `python manage.py init`
- **反向生成命令**: `backend/mysystem/management/commands/get_init_data.py` — 从数据库读取已有数据生成初始化代码

## 执行方式

### 整体初始化（全部执行）
```bash
cd dvlyadmin-mini\backend
python manage.py init          # 跳过已有数据
python manage.py init -y       # 先删除再重新创建
```

`manage.py init` 会遍历 `INSTALLED_APPS`，对每个 app 尝试执行 `from {app}.initialize import main; main(is_delete=...)`。

### 单独初始化某个方法
在 Django shell 中手动调用：
```bash
python manage.py shell -c "from mysystem.initialize import Initialize; Initialize().init_dept()"
```

### 获取数据库已有数据（反向生成初始化代码）
```bash
python manage.py get_init_data mysystem.Dept
python manage.py get_init_data mysystem.Menu
python manage.py get_init_data mysystem.Role
```
此命令会输出模型数据为 Python dict 格式，可直接复制到 `initialize.py` 中使用。

可选参数：
- `--fields name,key` 只获取指定字段
- `--exclude sort` 排除指定字段（默认已排除：create_datetime, update_datetime, is_delete, modifier, dept_belong）
- `--order_by sort` 按指定字段排序（默认：id）

---

## 添加新初始化数据的步骤

### 1. 在 Initialize 类中添加 init 方法

方法命名规则：`init_{名称}`，如 `init_brand`

```python
def init_brand(self):
    """
    初始化品牌数据
    python manage.py get_init_data mysystem.Brand
    """
    data = [
        {
            'id': 'brand_001',             # 必须指定固定ID，用于 update_or_create
            'creator_id': '0',             # creator_id='0' 表示系统创建
            'name': '品牌名称',
            'sort': 1,
            'status': True,
        },
        # ... 更多数据
    ]
    self.save(Brand, data, "品牌数据")
```

### 2. 在 Initialize.run() 中注册

在 `run()` 方法中添加调用（注意顺序，有依赖关系的放后面）：

```python
def run(self):
    try:
        self.init_dept()
        self.init_button()
        self.init_menu()
        # ... 已有的 init 方法
        self.init_brand()   # 新增
        print("所有初始化完成!")
    except Exception as e:
        print(f"初始化过程中出错: {str(e)}")
```

### 3. 在文件顶部导入模型

```python
from mysystem.models import Dept, Button, Menu, MenuButton, Role, Users, Brand
```

---

## save() 方法规则

`self.save(obj, data, name)` 是通用保存方法，核心逻辑：

```python
for ele in data:
    m2m_dict = {}   # 所有 list 类型的值
    new_data = {}   # 所有非 list 类型的值

    for key, value in ele.items():
        if isinstance(value, list):
            m2m_dict[key] = value
        else:
            new_data[key] = value

    # 用非 list 字段做 update_or_create
    obj.objects.update_or_create(id=ele.get("id"), defaults=new_data)

    # list 字段自动调用 m2m_field.set()
    for key, m2m in m2m_dict.items():
        m2m_field = getattr(object, key)
        m2m_field.set(m2m)
```

**重要注意**：save() 方法将**所有 list 类型的值**都当作 ManyToManyField 处理，会调用 `field.set()`。因此：

| 字段类型 | 正确做法 |
|---------|---------|
| 普通字段（str/int/bool/dict） | 直接赋值，放在 data dict 中 |
| ManyToManyField | 用 list 传关联对象的 ID 列表 |
| JSONField（值为 dict） | 直接用 Python dict 赋值 |
| JSONField（值为 list） | **不能直接放在 data dict 中**，需要特殊处理（见下方说明） |

**JSONField 值为 list 的处理方式**：

由于 save() 会把所有 list 当作 m2m 处理，如果 JSONField 的值是 list，需要先保存再手动赋值：

```python
def init_my_data(self):
    data = [
        {'id': '1', 'name': '测试', 'tags_id': ['tag1', 'tag2']},  # tags 是 m2m
    ]
    self.save(MyModel, data, "测试数据")

    # JSONField 值为 list 的，需要单独处理
    obj = MyModel.objects.get(id='1')
    obj.json_list_field = ['value1', 'value2']
    obj.save()
```

关键特性：
- 使用 `update_or_create(id=..., defaults=...)` — 有则更新，无则创建
- `delete=True` 时先删除 data 中所有 id 对应的记录再重新创建
- 每条记录独立 try/except，单条失败不影响其余

---

## 数据 ID 规范

- 必须为每条数据指定固定 ID（如 `'brand_001'`），确保重复执行不会产生重复数据
- `creator_id` 设为 `'0'` 表示系统级数据
- 外键字段使用 `{field}_id` 格式（如 `parent_id`、`role_id`）
- ID 命名建议：`{模块缩写}_{类型缩写}_{序号}`，如 `brand_001`、`menu_001`

## 现有初始化方法参考

```python
def init_dept(self):           # 部门信息
def init_button(self):         # 权限按钮标识
def init_menu(self):           # 菜单表
def init_menu_button(self):    # 菜单权限按钮
def init_role(self):           # 角色
def init_users(self):          # 用户
def init_notification(self):   # 通知
def init_notification_users(self):  # 通知用户
def init_systemconfig(self):   # 系统配置
def init_dictionary(self):     # 字典管理
```

## 反向操作：从数据库生成初始化数据

1. 先在 Django Admin 或 API 中手动创建数据
2. 运行 `python manage.py get_init_data mysystem.ModelName` 获取 dict 格式数据
3. 将输出复制到 `initialize.py` 的 `init_xxx` 方法中
