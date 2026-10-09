# -*- coding: utf-8 -*-
"""
@Remark: 全局 JSON 渲染器 —— 线上环境自动改写库内残留的本机回环图片/文件地址

背景：上传文件时（utils/file_upload.py）按当时的 DOMAIN_HOST 固化完整 URL 入库，
开发环境录入的数据会残留 http://127.0.0.1:8000/media/... 形式的地址；
线上部署后这些地址对浏览器不可达，逐条清洗数据库不可逆且开发/线上共库时会互相污染。

方案（出栈改写）：JSON 响应渲染前递归扫描，把回环地址前缀替换为当前 DOMAIN_HOST。
- 开发环境：DOMAIN_HOST 本身是回环地址 → 不改写，原样返回（本机可直接访问）
- 线上环境：DOMAIN_HOST 为真实域名 → 127/localhost 地址自动替换为线上域名
- 不依赖 DEBUG 标志：即使线上误开 DEBUG 也能正确改写，行为只取决于 DOMAIN_HOST 配置
- 误伤面：仅命中带 http(s):// 前缀的回环 URL；纯 IP 字符串（如 client_ip）不会被修改
"""
import re

from rest_framework.renderers import JSONRenderer

from config import DOMAIN_HOST

# 库内历史数据可能残留的本机回环地址前缀（含任意端口）
_LOOPBACK_RE = re.compile(r'https?://(?:127\.0\.0\.1|localhost)(?::\d+)?')

_DOMAIN = (DOMAIN_HOST or '').rstrip('/')
# DOMAIN_HOST 本身是回环地址（=开发环境）时整体停用改写
_ENABLED = bool(_DOMAIN) and not _LOOPBACK_RE.fullmatch(_DOMAIN)


def _rewrite_str(value):
    # 快速子串预检：不含回环特征的字符串直接跳过正则
    if '127.0.0.1' in value or 'localhost' in value:
        return _LOOPBACK_RE.sub(_DOMAIN, value)
    return value


def rewrite_loopback(obj):
    """递归遍历响应数据，把字符串中的回环地址前缀替换为 DOMAIN_HOST（dict/list 原地替换）。"""
    if isinstance(obj, str):
        return _rewrite_str(obj)
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = rewrite_loopback(value)
        return obj
    if isinstance(obj, list):
        for i, item in enumerate(obj):
            obj[i] = rewrite_loopback(item)
        return obj
    if isinstance(obj, tuple):
        return tuple(rewrite_loopback(item) for item in obj)
    return obj


class LoopbackRewriteJSONRenderer(JSONRenderer):
    """JSON 渲染前统一改写回环地址（开发环境原样，线上替换为 DOMAIN_HOST）"""

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if _ENABLED and data is not None:
            data = rewrite_loopback(data)
        return super().render(data, accepted_media_type, renderer_context)
