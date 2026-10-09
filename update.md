# 更新日志

## v2.0.1（2026-10-09）

### 新增

- AGENTS.MD ai开发文件
- .env.prod 生产配置模板和 .env.dev 开发配置模板 ，用于集成部署模式
- 默认使用sqlite3数据库
- 如果图片地址为127.0.0.1，线上生产环境部署，会自动根据config.py的DOMAIN_HOST配置，替换为线上域名。
- 适配RuYi Workstation 一键部署功能，方便快速发布和更新dvlydmin项目到RuYi-Panel如意面板
- 新增.trae下skills用于快速开发dvlyadmin和美化前端页面。

### 优化

- 重构优化前端管理页面，更符合现代审美UI
- 重构前端登录页面，更符合企业登录规范。

### 修复

- 修复前端权限页面点击事件bug