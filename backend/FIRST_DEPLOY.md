# dvlyadmin-mini 集成部署首次启动指南（非 Docker：如意面板/宝塔等）

> 适用场景：把 `backend/` 整个目录拷贝到服务器 Python 项目目录、新建静态反代的集成部署方式。
> 环境变量配置说明见同目录 [ENVIRONMENT.md](ENVIRONMENT.md)。

## 一、部署前置（本地 / 服务器）

### 1. 前端构建产物（本地执行）

```bash
cd dvlyadmin-mini/frontend
npm run build:backend
```

产物自动输出到 `backend/frontend/lyadmin/`，随 backend 目录一起拷贝到服务器（`urls.py` 的 TemplateView 渲染该目录的 `index.html`）。

### 2. 拷贝代码到服务器

把 `backend/` 全部内容拷到面板 Python 项目目录。

> **注意**：如果服务器上已配置过 `.env`（真实密钥），拷贝时务必排除它，不要被本地文件覆盖或因"清空目录再拷"而丢失。

### 3. 配置环境变量（首次执行一次）

```bash
cp .env.prod .env
vi .env   # 填入真实数据库密码、SMTP 授权码等敏感项
```

### 4. 安装 Python 依赖

```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

## 二、首次启动四步（按顺序执行）

> 以下命令均在服务器项目目录（`manage.py` 所在处）执行。
> 前提：`.env` 已配置好数据库连接。

### 第 1 步：生成迁移文件（makemigrations）

```bash
python manage.py makemigrations
```

**注意**：迁移文件已随代码提交，正常情况此步应输出 `No changes detected`（仅做校验）。
如果它**生成了新文件**，说明代码里缺少迁移——先确认拷贝是否完整，不要在服务器上随手生成后跳过。

### 第 2 步：执行数据库迁移（migrate）

```bash
python manage.py migrate
```

### 第 3 步：初始化数据（init，仅首次）

```bash
python manage.py init
```

写入菜单、角色、按钮权限、系统配置等种子数据，并创建初始管理员：

- 账号：`superadmin`　密码：`123456`
- **首次登录后立即修改密码**

重复执行是幂等的（按固定 id `update_or_create`），但正常只在首次启动跑一次。

### 第 4 步：收集静态文件（collectstatic）

```bash
python manage.py collectstatic
```

把 Django 后台 / DRF / Swagger 的静态文件收集到 `STATIC_ROOT`（即 `backend/static/`），由 `urls.py` 的 `path('static/<path:path>', serve, ...)` 对外提供。

**不执行的现象**：`/static/...` 全部 404，登录页样式丢失（但首页白屏也可能与前端产物未就位有关，两者路径不同：前端产物在 `frontend/lyadmin/`，collectstatic 产物在 `static/`）。

## 三、启动服务

```bash
# 开发调试方式
python manage.py runserver 127.0.0.1:8000

# 生产方式：ASGI（支持 WebSocket），面板中按此配置启动命令
daphne -b 0.0.0.0 -p 8000 --proxy-headers application.asgi:application
```

其他方式请按具体面板的正确方式启动部署即可
