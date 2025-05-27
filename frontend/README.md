# dvlyadmin-mini前端

vue3+vite+elementplus

## 安装依赖

```
npm install --registry=https://registry.npmmirror.com
```

## 本地开发-启动方式

```
npm start
```

## 打包线上

### 单独打包

```
npm run build
```

注意：默认打包后的静态文件位置：```backend/frontend/admin``` 目录中

### 集成部署打包

```
npm run build:backend
```

注意：此命令会把打包后的静态文件复制到：```backend/frontend/admin``` 目录中，方面与后端集成部署

## 疑问

1. 怎么自定义的icon？

答：把自定义的svg文件放入```src/assets/lybbn/icons/svg```中即可

2. 前端配置文件在哪？

答：在```src/config/index.js```中，具体内容都有注释