# dvlyadmin-mini 精简版介绍

## 🌟 简介

**dvlyadmin-mini** 是专为追求页面极致效果的开发者设计的一套 **django-vue-lyadmin** 优化升级的精简版。我们通过大量重构架构，去除了无用冗余代码，力求做到小而精。前端采用 **Vite + Vue 3 + Element Plus**，支持适配手机端，助力快速开发项目及提升项目质量！

### 主要特性：

- 💻 **前端技术栈**：Vue 3 + Setup JS + Pinia + Element Plus
- 🖥️ **后端技术栈**：Python 语言 Django 框架以及强大的 [Django REST Framework](https://pypi.org/project/djangorestframework)
- 🔒 **认证系统**：使用 [Django REST Framework SimpleJWT](https://pypi.org/project/djangorestframework-simplejwt)，支持多终端认证系统
- ⚙️ **权限管理**：支持加载动态权限菜单，提供多种方式轻松实现权限控制
- 📊 **列权限管控**：全新的列权限管理机制，粒度细化到每一列
- ⚡️ **CRUD**：全新设计CRUD页面，适合快速开发CRUD页面，喜欢基于配置或深度自定义的页面的小伙伴
---

## 💻 技术栈

### 前端

- **构建工具**：[Vite](https://vitejs.dev/)
- **框架**：[Vue 3](https://vuejs.org/)
- **UI 组件库**：[Element Plus](https://element-plus.org/)
- **编程模式**：JavaScript Setup 语法

---

## 💪 优势

1. **页面简洁美观** - 极致的设计理念，带来清爽的视觉体验，搜索框多行默认显示一行，然后手动展开和收起，避免搜索暂用过多。
2. **响应式设计** - 完美适配手机端，随时随地高效工作。
3. **代码精简高效** - 开发项目时基本无需再删减代码，专注于业务逻辑。
4. **更全的注释** - 前后端更多的代码注释，帮助你快速了解和修改代码功能。
5. **适配大多数据库** - 无需导入sql文件，直接init命令初始化数据，可自由更换数据库类型。
---

## ❓ 常见问题解答

### 能否与 django-vue-lyadmin 完美契合？

**答**：虽然 dvlyadmin-mini 在设计理念上与 django-vue-lyadmin 相似，但由于它采用了 **Vite** 进行构建，并且在框架方面进行了完全重构，因此不能直接替换原有的 django-vue-lyadmin。不过，两者在使用方式上有很大的相似性，如果你熟悉 django-vue-lyadmin，那么过渡到 dvlyadmin-mini 将会非常顺畅。

### 添加菜单注意事项？

**答**：添加菜单时路由和组件名称最好与新建的菜单文件名一致，会自动发现并注册路由，无需填写【组件路径】，否则需填写此项！！！

### 如何快速实现导出功能？

**答**：继承了CustomModelViewSet方法的都会自动生成export_data接口，默认使用前端导出字段和serializer_class作为导出参数,也可单独配置export_serializer_class和export_field_dict实现导出自定义！！！

---

### 额外提示

- 如果你希望进一步定制或扩展你的应用，[dvlyadmin_pro](https://doc.lybbn.cn/support/subscribe.html) 提供了更丰富的功能，确保你能快速上手并进行个性化调整。

---

### 目录介绍

```
backend/                # 后端代码目录
frontend/               # 前端代码目录
```