# ================================================= #
# ************** mysql数据库 配置  ************** #
# ================================================= #
import os
import sys


def _load_env_file(path):
    """加载指定的 .env 环境变量文件（不覆盖真实环境变量）。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                if line.startswith("export "):
                    line = line[7:].lstrip()
                key, _, value = line.partition("=")
                key, value = key.strip(), value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                    value = value[1:-1]
                if key and key not in os.environ:
                    os.environ[key] = value
    except OSError:
        pass  # 文件不存在或不可读时静默忽略，走默认值


def _select_env_file():
    """多环境配置档案选择（优先级从高到低，命中即停）：

    1. backend/.env          —— 当前部署实际生效的配置（服务器上 cp 自 .env.prod；
                                Docker 由 entrypoint 提前 source，此处自动跳过已有变量，双保险）
    2. .env.{DVLYADMIN_ENV}  —— 通过真实环境变量 DVLYADMIN_ENV 显式指定环境档案
                                （如 DVLYADMIN_ENV=prod 加载 .env.prod），适合同机多套环境切换
    3. backend/.env.dev      —— 本地开发默认档案
    都不存在时走本文件各默认值（即开发配置），与无 .env 机制前行为一致。
    """
    base = os.path.dirname(os.path.abspath(__file__))
    explicit = os.path.join(base, ".env")
    if os.path.exists(explicit):
        return explicit
    profile = os.environ.get("DVLYADMIN_ENV", "").strip()
    if profile:
        if profile.replace("_", "").replace("-", "").isalnum():
            path = os.path.join(base, f".env.{profile}")
            if os.path.exists(path):
                return path
        print(f"[config] 警告：DVLYADMIN_ENV={profile} 对应的 .env.{profile} 不存在，回退开发档案", file=sys.stderr)
    dev = os.path.join(base, ".env.dev")
    if os.path.exists(dev):
        return dev
    return None


_env_file = _select_env_file()
if _env_file:
    _load_env_file(_env_file)

# 数据库类型 MYSQL/SQLITE3/POSTGRESQL
# 环境变量统一加 DVLYADMIN_ 前缀，避免与 MySQL 官方镜像内置变量冲突
DATABASE_TYPE = os.environ.get("DVLYADMIN_DATABASE_TYPE", "MYSQL")
# 数据库地址
DATABASE_HOST = os.environ.get("DVLYADMIN_DATABASE_HOST", "127.0.0.1")
# 数据库端口
DATABASE_PORT = int(os.environ.get("DVLYADMIN_DATABASE_PORT", 3306))
# 数据库用户名
DATABASE_USER = os.environ.get("DVLYADMIN_DATABASE_USER", "root")
# 数据库密码
DATABASE_PASSWORD = os.environ.get("DVLYADMIN_DATABASE_PASSWORD", "root")
# 数据库名
DATABASE_NAME = os.environ.get("DVLYADMIN_DATABASE_NAME", "dvlyadmin_mini")

# ================================================= #
# ************** redis 配置  ************** #
# ================================================= #
# 本地无 Redis 时，可设置 DVLYADMIN_CACHE_LOCMEM=true 使用内存缓存
CACHE_LOCMEM = os.environ.get("DVLYADMIN_CACHE_LOCMEM", "True").lower() == "true"

REDIS_PASSWORD = os.environ.get("DVLYADMIN_REDIS_PASSWORD", '')
REDIS_HOST = os.environ.get("DVLYADMIN_REDIS_HOST", '127.0.0.1')
REDIS_PORT = os.environ.get("DVLYADMIN_REDIS_PORT", '6379')
REDIS_URL = f'redis://:{REDIS_PASSWORD or ""}@{REDIS_HOST}:{REDIS_PORT}'

# ================================================= #
# ************** 服务器基本 配置  ************** #
# ================================================= #

#全局控制日志记录
API_LOG_ENABLE = True
API_LOG_METHODS = ['POST', 'UPDATE', 'DELETE', 'PUT']  # ['POST', 'DELETE']

IS_DEMO = os.environ.get("DVLYADMIN_IS_DEMO", "False").lower() == "true" #是否演示模式（演示模式只能查看无法保存、编辑、删除、新增）
DEBUG = os.environ.get("DVLYADMIN_DEBUG", "True").lower() == "true" #是否调试模式
ALLOWED_HOSTS = ["*"]
IS_SINGLE_TOKEN = False #是否只允许单用户单一地点登录(只有一个人在线上)(默认多地点登录),只针对后台用户生效
ALLOW_FRONTEND = True#是否关闭前端API访问
LOGIN_ERROR_RETRY_TIMES = 0 #登录错误次数限制，0表示不限制
LOGIN_ERROR_RETRY_TIMEOUT = 60 #登录错误次数过期时间，单位秒
FRONTEND_API_LIST = ['/api/app/','/api/xcx/','/api/h5/']#微服务前端接口前缀
DOMAIN_HOST = os.environ.get("DVLYADMIN_DOMAIN_HOST", "http://127.0.0.1:8000")#控制图片上传后保存所使用到的url前缀

# ================================================= #
# ************** 邮件配置 ************** #
# ================================================= #
# 可直接修改下面的默认值，也可通过 DVLYADMIN_ 前缀环境变量覆盖。
# 开发环境默认将邮件输出到控制台；生产环境默认使用 SMTP。
EMAIL_BACKEND = os.environ.get(
    "DVLYADMIN_EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = os.environ.get("DVLYADMIN_EMAIL_HOST", "smtp.163.com")
EMAIL_PORT = int(os.environ.get("DVLYADMIN_EMAIL_PORT", 25))
EMAIL_HOST_USER = os.environ.get("DVLYADMIN_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("DVLYADMIN_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("DVLYADMIN_EMAIL_USE_TLS", "False").lower() == "true"
DEFAULT_FROM_EMAIL = os.environ.get("DVLYADMIN_DEFAULT_FROM_EMAIL", "")

#自定义接口权限
CUSTOM_PERMISSION_CAHCE = False #是否启用权限缓存，增强性能
CUSTOM_PERMISSION_CAHCE_TIME = 60 * 60 #缓存时间 1 小时
CUSTOM_PERMISSION_WHITELIST = {
    ('/api/system/menu/web_router/', 'GET'),
    ('/api/system/menu_button/menu_button_permission/', 'GET'),
    ('/api/schema/lyjson/', 'GET'),
    ('/api/system/menu_field/get_models/','GET')
}#前端也可配置，两者建议后端直接配置，更高效

#自定义数据权限
DATA_FILTER_CACHE = False #是否启用数据权限缓存，增强性能
DATA_FILTER_CAHCE_TIME = 60 * 60 #缓存时间 1 小时

#列权限
FIELD_PERMISSION_CACHE = False #是否开启列权限缓存
