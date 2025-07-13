# ================================================= #
# ************** mysql数据库 配置  ************** #
# ================================================= #
# 数据库类型 MYSQL/SQLITE3/POSTGRESQL
DATABASE_TYPE = "MYSQL"
# 数据库地址
DATABASE_HOST = "127.0.0.1"
# 数据库端口
DATABASE_PORT = 3306
# 数据库用户名
DATABASE_USER = "root"
# 数据库密码
DATABASE_PASSWORD = "root"
# 数据库名
DATABASE_NAME = "dvlyadmin_mini"

# ================================================= #
# ************** redis 配置  ************** #
# ================================================= #

REDIS_PASSWORD = ''
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_URL = f'redis://:{REDIS_PASSWORD or ""}@{REDIS_HOST}:{REDIS_PORT}'

# ================================================= #
# ************** 服务器基本 配置  ************** #
# ================================================= #

#全局控制日志记录
API_LOG_ENABLE = True
API_LOG_METHODS = ['POST', 'UPDATE', 'DELETE', 'PUT']  # ['POST', 'DELETE']

IS_DEMO = False #是否演示模式（演示模式只能查看无法保存、编辑、删除、新增）
DEBUG = True #是否调试模式
ALLOWED_HOSTS = ["*"]
IS_SINGLE_TOKEN = False #是否只允许单用户单一地点登录(只有一个人在线上)(默认多地点登录),只针对后台用户生效
ALLOW_FRONTEND = True#是否关闭前端API访问
LOGIN_ERROR_RETRY_TIMES = 0 #登录错误次数限制，0表示不限制
LOGIN_ERROR_RETRY_TIMEOUT = 60 #登录错误次数过期时间，单位秒
FRONTEND_API_LIST = ['/api/app/','/api/xcx/','/api/h5/']#微服务前端接口前缀
DOMAIN_HOST = "http://127.0.0.1:8000"#控制图片上传后保存所使用到的url前缀

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