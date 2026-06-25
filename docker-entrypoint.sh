#!/bin/sh
# ========================================================= #
# dvlyadmin-mini Docker 容器启动脚本
# 流程：等待 MySQL 就绪 -> 执行 migrate -> 初始化数据 -> 启动 daphne
# ========================================================= #
set -e

echo "==> [dvlyadmin-mini] 启动入口脚本"

# ---------------- 持久化目录初始化 ----------------
# 软链接已在 Dockerfile 构建时创建；此处仅确保挂载卷的子目录存在
mkdir -p /app/backend/data/media /app/backend/data/logs

# ---------------- 等待 MySQL 就绪 ----------------
MAX_WAIT=120
WAITED=0
until mysqladmin ping -h "${DVLYADMIN_DATABASE_HOST:-mysql}" -P "${DVLYADMIN_DATABASE_PORT:-3306}" \
        -u"${DVLYADMIN_DATABASE_USER:-root}" -p"${DVLYADMIN_DATABASE_PASSWORD:-root}" --silent 2>/dev/null; do
    WAITED=$((WAITED + 2))
    if [ "$WAITED" -ge "$MAX_WAIT" ]; then
        echo "    [错误] 等待 MySQL 超时（${MAX_WAIT}s），退出。"
        exit 1
    fi
    echo "    等待 MySQL 就绪... (${WAITED}s)"
    sleep 2
done
echo "==> [dvlyadmin-mini] MySQL 已就绪"

# ---------------- 执行数据库迁移 ----------------
echo "==> [dvlyadmin-mini] 执行 migrate"
python manage.py migrate --noinput

# ---------------- 初始化数据（仅首次） ----------------
# 通过标记文件避免重复初始化，标记文件放在挂载卷内，容器重建不丢失
INIT_FLAG="/app/backend/data/.initialized"
RUN_INIT="${DVLYADMIN_RUN_INIT:-true}"
if [ "$RUN_INIT" = "true" ] && [ ! -f "$INIT_FLAG" ]; then
    echo "==> [dvlyadmin-mini] 执行 init 初始化数据"
    python manage.py init && touch "$INIT_FLAG" || echo "    [警告] init 执行失败，可手动执行 python manage.py init"
else
    echo "==> [dvlyadmin-mini] 跳过初始化（已初始化或 RUN_INIT!=true）"
fi

# ---------------- 再次收集静态文件（覆盖前端产物） ----------------
echo "==> [dvlyadmin-mini] collectstatic"
python manage.py collectstatic --noinput || true

# ---------------- 启动应用 ----------------
echo "==> [dvlyadmin-mini] 启动应用：$@"
exec "$@"
