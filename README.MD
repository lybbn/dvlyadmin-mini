# dvlyadmin-mini 介绍

[![img](https://img.shields.io/badge/python-%3E=3.11.x-green.svg)](https://python.org/)  [![PyPI - Django Version badge](https://img.shields.io/badge/django%20versions-%3E%3D%204.x-blue)](https://docs.djangoproject.com/zh-hans/4.1/) [![img](https://img.shields.io/badge/node-%3E%3D%2014.0.0-brightgreen)](https://nodejs.org/zh-cn/) [![img](https://gitee.com/lybbn/dvlyadmin-mini/badge/star.svg?theme=dark)](https://gitee.com/lybbn/dvlyadmin-mini)

[在线预览](https://dvlyadmin-mini.lybbn.cn) | [官网文档](https://doc.lybbn.cn/dvlyadmin_mini/introduce.html)| [关于授权](https://doc.lybbn.cn/dvlyadmin_mini/subscribe.html)

## 🌟 简介

**dvlyadmin-mini** 是专为追求页面极致效果的开发者设计的一套 **django-vue-lyadmin** 优化升级的精简版。我们通过大量重构架构，去除了无用冗余代码，力求做到小而精。前端采用 **Vite + Vue 3 + Element Plus**，支持适配手机端，助力快速开发项目及提升项目质量！

## 🚀 在线体验

<div style="border-left: 4px solid #3498db; padding-left: 1em; margin: 1em 0;">
  <table>
    <tr>
      <td><strong>🌍 访问地址</strong></td>
      <td><a href="https://dvlyadmin-mini.lybbn.cn" target="_blank" rel="noreferrer">https://dvlyadmin-mini.lybbn.cn</a></td>
    </tr>
    <tr>
      <td><strong>👤 测试账号</strong></td>
      <td><code>admin</code></td>
    </tr>
    <tr>
      <td><strong>🔑 登录密码</strong></td>
      <td><code>123456</code></td>
    </tr>
  </table>
</div>

## 💡 交流

- QQ群号：

1. django-vue-lyadmin交流01群(已满)：755277564
1. django-vue-lyadmin交流02群：877020250 <a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=bQteR0foj1tZuZE0kdVF3XV9xozOmr9p&jump_from=webapi&authKey=8GRzb/ATMG1hXE7G1n2oCHyoHrP0+mg7xBzskR6mnw8eqb9LTv6FuAhHtoqs2F3y"><img border="0" src="//pub.idqqimg.com/wpa/images/group.png" alt="点击链接加入群聊" title="django-vue-lyadmin交流02群"></a>

## 🎨 主要特性：

- 💻 **前端技术栈**：Vue 3 + Setup JS + Pinia + Element Plus
- 🖥️ **后端技术栈**：Python 语言 Django 框架以及强大的 [Django REST Framework](https://pypi.org/project/djangorestframework)
- 🔒 **认证系统**：使用 [Django REST Framework SimpleJWT](https://pypi.org/project/djangorestframework-simplejwt)，支持多终端认证系统
- ⚙️ **权限管理**：支持加载动态权限菜单，提供多种方式轻松实现权限控制
- 📊 **列权限管控**：全新的列权限管理机制，粒度细化到每一列
- ⚡️ **CRUD增强**：全新设计CRUD页面，适合快速开发CRUD页面，喜欢基于配置或深度自定义的页面的小伙伴
---

## 💻 技术栈

### 前端

- **构建工具**：[Vite（极速构建）](https://vitejs.dev/)
- **框架**：[Vue 3（组合式 API）](https://vuejs.org/)
- **UI 组件库**：[Element Plus （企业级 UI）](https://element-plus.org/)
- **编程模式**：JavaScript Setup 语法糖

### 后端

- **Python**：>=Python3.11.x
- **Django**：>=Django4.x
- **DRF**：Django REST Framework
- **JWT**：Django REST Framework SimpleJWT

---

## 💪 核心优势

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

### 专业版推荐

- 如果你希望进一步定制或扩展你的应用，[dvlyadmin_pro](https://doc.lybbn.cn/support/subscribe.html) 提供了更丰富的功能，确保你能快速上手并进行个性化调整。

---

### 目录介绍

```
backend/                # 后端代码目录
frontend/               # 前端代码目录
```

## ✅ 演示图

![登录](https://foruda.gitee.com/images/1752461064099761356/404e5c89_4823422.png "wechat_2025-07-14_104123_881.png")
![首页](https://foruda.gitee.com/images/1752461080317609620/bbc20f96_4823422.png "wechat_2025-07-14_104159_622.png")
![个人中心](https://foruda.gitee.com/images/1752461095093419420/509ffd91_4823422.png "wechat_2025-07-14_104208_520.png")
![用户管理](https://foruda.gitee.com/images/1752461107939022968/53d97e3d_4823422.png "wechat_2025-07-14_104237_798.png")
![菜单管理](https://foruda.gitee.com/images/1752461123060391528/e0e5573d_4823422.png "wechat_2025-07-14_104252_982.png")
![权限管理](https://foruda.gitee.com/images/1752461137054532488/065360f7_4823422.png "wechat_2025-07-14_104304_906.png")
![操作日志](https://foruda.gitee.com/images/1752461150156275848/b71b3e88_4823422.png "wechat_2025-07-14_104319_022.png")
![系统配置](https://foruda.gitee.com/images/1752461163988365301/7817a2e2_4823422.png "wechat_2025-07-14_104328_836.png")
![字典管理](https://foruda.gitee.com/images/1752461182186356276/8ff97750_4823422.png "wechat_2025-07-14_104336_924.png")