## 📌 注意事项
- 默认安装 `django==4.1.8` 可支持 MySQL 5.7
- 如需支持 MySQL 8.x 及以上版本，请使用最新版 Django（修改 `requirements.txt`）

## 安装依赖环境

```
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

## 🛠️执行迁移命令：(使用sql脚本直接导入可忽略本步骤)

```
# 生成迁移文件
python manage.py makemigrations
# 执行迁移
python manage.py migrate
```

## 📊初始化数据：(使用sql脚本直接导入可忽略本步骤)

```
python manage.py init
```

## 🚦启动项目（初始账号：superadmin 密码：123456）

```
#开发服务器方式
python manage.py runserver 127.0.0.1:8000

#ASGI 部署方式（支持 WebSocket）
或使用 daphne (使用【终端服务】的需要使用此asgi方式部署来支持websocket):

daphne -b 0.0.0.0 -p 8000 --proxy-headers application.asgi:application

#异步任务celery启动
如需使用celery【计划任务】，还需要额外启动celery 和 beat（调度器）

mac/linux:
celery -A application worker -B -l info

windows:(需要安装: pip install eventlet)
celery -A application worker -P eventlet -l info
celery -A application beat -l info

```