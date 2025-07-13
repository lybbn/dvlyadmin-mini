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

注意：默认打包后的静态文件位置：```backend/frontend/lyadmin``` 目录中

### 集成部署打包

```
npm run build:backend
```

注意：此命令会把打包后的静态文件复制到：```backend/frontend/lyadmin``` 目录中，方面与后端集成部署

## 疑问

1. 怎么自定义的icon？

答：把自定义的svg文件放入```src/assets/lybbn/icons/svg```中即可

2. 前端配置文件在哪？

答：在```src/config/index.js```中，具体内容都有注释

### 目录介绍

```
src/
├── api/                # API请求
│   ├── api.js          # 接口API
│   ├── request.js      # web请求封装
├── assets/             # 静态资源文件
├── components/         # 公共组件
├── config/             # 系统配置
│   └── index.js
├── router/             # 路由配置
│   └── index.js
├── store/              # pinia状态管理
│   ├── keepAlive.js    # 缓存模块
│   ├── cancelRequest.js# 页面离开取消请求模块
│   ├── websocket.js    # websocket模块
│   └── index.js
├── utils/              # 工具函数
│   ├── directive.js    # 命令封装
│   ├── message.js      # 消息封装
│   └── util.js         # 公共方法封装
├── layout/             # 布局组件
├── views/              # 页面组件
│   ├── system/         # 系统页面
└── main.js             # 主入口文件

```