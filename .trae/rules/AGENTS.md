# 项目全局规则

## 行为约束

### Django Migration 文件保护

**核心原则：严禁直接修改 migrations 目录下的任何文件。**

Migration 文件是 Django 数据库迁移的记录，必须通过 Django 的迁移系统自动管理。

#### 允许的操作

1. ✅ **运行 makemigrations 命令** - 自动生成迁移文件
2. ✅ **读取和分析 migration 文件** - 了解迁移历史
3. ✅ **提供意见和建议** - 分析模型变更，建议优化方案

#### 禁止的操作

1. ❌ **直接编辑 migration 文件** - 不修改 operations、dependencies 等
2. ❌ **删除 migration 文件** - 不删除任何已存在的迁移文件
3. ❌ **手动创建 migration 文件** - 不手动编写迁移文件内容

#### 正确流程

当模型发生变更时：
1. 分析 models.py 中的变更
2. 告知用户需要创建迁移
3. 运行 `python manage.py makemigrations <app_name>`
4. 展示生成的 migration 文件供用户确认

### 适用范围

此规则适用于所有 migrations 目录：
- `backend/bkmanage/backend/apps/*/migrations/`

---
