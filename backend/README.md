
## 安装依赖环境

pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

## 执行迁移命令：(使用sql脚本直接导入可忽略本步骤)

python manage.py makemigrations
python manage.py migrate

## 初始化数据：(使用sql脚本直接导入可忽略本步骤)

python manage.py init

## 启动项目（初始账号：superadmin 密码：123456）

python manage.py runserver 127.0.0.1:8000

或使用 daphne (使用【终端服务】的需要使用此asgi方式部署来支持websocket):

daphne -b 0.0.0.0 -p 8000 --proxy-headers application.asgi:application

使用celery【计划任务】需要额外启动celery 和 beat（调度器）

mac/linux:
celery -A application worker -B -l info

windows:(需要安装: pip install eventlet)
celery -A application worker -P eventlet -l info
celery -A application beat -l info