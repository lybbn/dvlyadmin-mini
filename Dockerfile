# ========================================================= #
# 多阶段构建：阶段1 - 构建前端（Vue3 + Vite） 集成部署到dvlyadmin-mini的后端
# ========================================================= #
FROM node:26-alpine AS frontend-builder

WORKDIR /app/frontend

# 设置 npm 淘宝镜像加速
RUN npm config set registry https://registry.npmmirror.com

# 先拷贝依赖清单，利用 Docker 缓存层
COPY frontend/package.json frontend/package-lock.json* ./

# 安装依赖（如果无 package-lock.json 则使用 npm install）
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# 拷贝前端源码并构建（仅执行 vite build，产物在 dist/）
COPY frontend/ ./
RUN npm run build


# ========================================================= #
# 多阶段构建：阶段2 - 后端运行环境（Python + Django/Daphne）
# ========================================================= #
FROM python:3.12-slim-bookworm

# 设置时区为上海，匹配项目 TIME_ZONE
ENV TZ=Asia/Shanghai \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# 安装系统依赖（mysqlclient 编译依赖 + 常用工具）
# 替换 apt 源为阿里云镜像，加速国内下载
    RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources \
    && sed -i 's|security.debian.org/debian-security|mirrors.aliyun.com/debian-security|g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update && apt-get install -y --no-install-recommends \
        default-mysql-client \
        tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend

# 先安装 Python 依赖（利用缓存层）
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 拷贝后端代码
COPY backend/ ./

# 从前端构建阶段拷贝构建产物到集成部署目录
# 项目约定：前端构建产物放到 backend/frontend/lyadmin（由 urls.py 中 TemplateView 渲染）
COPY --from=frontend-builder /app/frontend/dist/ ./frontend/lyadmin/

# 创建持久化目录软链接（构建时固定，运行时挂载卷后子目录由 entrypoint 创建）
# 宿主只需挂载 /app/backend/data 一个目录，media/logs 软链到其子目录，实现统一持久化
# 注意：COPY backend/ 会把 media/logs 目录（.dockerignore 仅排除内容）创建为真实空目录，
# 若不先删除，ln -sf 遇到真实目录会在其内部创建链接，导致 media/media 嵌套
RUN rm -rf /app/backend/media /app/backend/logs \
    && ln -s /app/backend/data/media /app/backend/media \
    && ln -s /app/backend/data/logs /app/backend/logs

# 拷贝启动脚本并赋权
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# 拷贝 .env.docker 到 backend 目录，供启动时加载环境变量
COPY .env.docker /app/backend/.env

# 收集 Django 静态文件到 STATIC_ROOT（需在依赖与代码就绪后执行）
RUN python manage.py collectstatic --noinput || true

# 暴露端口（daphne 服务端口）
EXPOSE 8000

# 持久化挂载点（宿主只需挂载这一个目录，media/logs 启动时软链到其子目录）
VOLUME ["/app/backend/data"]

# 启动时先加载 /app/backend/.env 环境变量，再执行入口脚本
# 末尾的 "sh" 作为 $0，CMD 参数通过 "$@" 透传给 docker-entrypoint.sh
ENTRYPOINT ["sh", "-c", "set -a; . /app/backend/.env; set +a; exec /usr/local/bin/docker-entrypoint.sh \"$@\"", "sh"]

# 默认使用 daphne 以支持 WebSocket（ASGI 部署）
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "--proxy-headers", "application.asgi:application"]
