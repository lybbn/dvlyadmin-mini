# -*- coding: utf-8 -*-

"""
@Author: lybbn
@QQ:1042594286
@EditDate: 2025-06-28
@Remark: 自定义文件上传
"""

import os
import datetime
from utils.common import renameuploadimg
from django.conf import settings
from config import DOMAIN_HOST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def ImageUpload(request, paramsname, dirs):
    """
    优化后的图片上传功能
    参数:
        request: 请求对象
        paramsname: formData中提交数据的名称，如：file
        dirs: 要上传到的目录
    返回:
        包含状态码、消息和图片URL的字典
    """
    # 初始化返回消息
    msg = {
        'code': 400,
        'msg': '',
        'img': []
    }
    
    # 验证上传文件是否存在
    if paramsname not in request.FILES:
        msg['msg'] = "上传的图片不能为空"
        return msg
        
    images = request.FILES.getlist(paramsname)
    if not images:
        msg['msg'] = "上传的图片不能为空"
        return msg

    # 支持的图片格式
    ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    notimg_files = []
    img_urls = []
    
    try:
        for img in images:
            # 验证文件类型
            if not img.content_type.startswith('image/'):
                notimg_files.append(img.name)
                continue
                
            # 验证文件扩展名
            ext = os.path.splitext(img.name)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                notimg_files.append(img.name)
                continue
                
            # 验证文件大小
            if img.size > MAX_FILE_SIZE:
                msg['msg'] = f"图片 {img.name} 大小不能超过50M"
                return msg
                
            # 生成存储路径
            curr_time = datetime.datetime.now()
            time_path = curr_time.strftime("%Y-%m-%d")
            new_filename = renameuploadimg(img.name)
            relative_path = os.path.join(dirs, time_path, new_filename)
            
            # 使用Django的存储API保存文件
            file_path = default_storage.save(relative_path, ContentFile(img.read()))
            
            # 构建完整的URL
            web_img_url = f"{DOMAIN_HOST}{settings.MEDIA_URL}{file_path}"
            img_urls.append(web_img_url)
            
        # 处理非图片文件提示
        if notimg_files:
            sample_files = ', '.join(notimg_files[:5])
            if len(notimg_files) > 5:
                sample_files += f" 等{len(notimg_files)}个文件"
            msg['msg'] = f"以下文件不是有效的图片格式: {sample_files}"
            return msg
            
        # 成功返回
        msg.update({
            'code': 200,
            'msg': '上传成功',
            'img': img_urls
        })
        
    except IOError as e:
        msg['msg'] = f"文件存储错误: {str(e)}"
    except Exception as e:
        msg['msg'] = f"图片上传失败: {str(e)}"
        
    return msg