#  Docker 部署

## 1. Docker 推送

```bash
docker build -f Dockerfile -t dvlyadmin-mini:latest .
docker images
docker tag bf8xxxxx registry.cn-beijing.aliyuncs.com/django-vue-lyadmin/dvlyadmin-mini:latest
docker push registry.cn-beijing.aliyuncs.com/django-vue-lyadmin/dvlyadmin-mini:latest
```

## 2. 部署到生产环境（运行容器）

```bash
docker pull registry.cn-beijing.aliyuncs.com/django-vue-lyadmin/dvlyadmin-mini:latest
docker run --restart unless-stopped -d --name dvlyadmin-mini -p 8000:8000 --add-host=host.docker.internal:host-gateway -v /opt/dvlyadmin-mini:/app/backend/data registry.cn-beijing.aliyuncs.com/django-vue-lyadmin/dvlyadmin-mini:latest
```

## 3. 直接一键打包部署

```bash
./build-and-push.bat
```
