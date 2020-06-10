# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from utils.helpers.jsonify import jsonify, get_post_req_data
from utils.helpers.decorators import check_post, check_login
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.shortcuts import render
from utils.helpers.uploadImage import save_block_file
from article.models import Article
from utils.constants import FILE_SAVE_PATH, OSS_URL
import os
import time
OSS_PATH = '/home/ubuntu/oss'
# 获取目录下所有文件
def DirAll(pathName, files): 
    if os.path.exists(pathName):
        fileList = os.listdir(pathName); 
        for f in fileList:
            data = {}
            if f=="$RECYCLE.BIN" or f=="System Volume Information":
                continue; 
            f=os.path.join(pathName,f);
            dirName=os.path.dirname(f); 
            baseName=os.path.basename(f); 
            data['name'] = baseName
            data['path'] = dirName
            if os.path.isdir(f):
                mtime = os.stat(pathName).st_mtime
                data['type'] = 'folder'
            else: 
                data['type'] = 'file'
                mtime = os.stat(dirName+os.sep+baseName).st_mtime

                #dirName=os.path.dirname(f); 
                #baseName=os.path.basename(f); 
                #if dirName.endswith(os.sep): 
                #    files.append(dirName+baseName); 
                #else: 
                #    files.append(dirName+os.sep+baseName); 
            #data['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
            data['time'] = int(mtime)
            files.append(data)
    return files



@require_POST
def imageUpload(request):
    """图片上传"""
    image = request.FILES.get("file")
    param = request.POST.get('param', 'common')
    if not image:
        return jsonify(data=None, success=False, errMsg='未找到图片文件')
    if param not in ['avatar', 'cover', 'content', 'common']:
        return jsonify(data=None, success=False, errMsg='param error.')

    try:
        service_name = save_block_file(image, param)
        print 'service_name: %s' %service_name
        return jsonify(data=service_name, success=True, errMsg='')
    except:
        import traceback
        traceback.print_exc()
        return jsonify(data=None, success=False, errMsg='Upload image failed.')



#@check_login
@check_post
def imageAll(req):
    """
    获取所有图片
    """
    pathName = req.POST.get('path', OSS_PATH)
    files = list()
    data = DirAll(pathName, files)
    return jsonify(data=data, success=True, errMsg='')

@check_login
@check_post
def removeFile(req):
    """
    删除文件
    """
    pathName = req.POST.get('path')
    cover_url = pathName.replace(FILE_SAVE_PATH, OSS_URL, 1)
    is_link_article = Article.objects.filter(cover_url= cover_url)
    print is_link_article
    if is_link_article:
        return jsonify(data=None, success=False, errMsg='文件正在被文章使用，无法删除!')

    if(os.path.exists(pathName)):
        os.remove(pathName)
        return jsonify(data=None, success=True, errMsg='')
    else:
        return jsonify(data=None, success=False, errMsg='文件不存在!')


@check_login
@check_post
def mkdir(req):
    """
    新建目录
    """
    path = req.POST.get('path')
    dirName = req.POST.get('dirName')
    print path
    print dirName
    print FILE_SAVE_PATH
    if not path or not dirName:
        return jsonify(data=None, success=False, errMsg='param error.')

    elif not os.path.exists(path):
        return jsonify(data=None, success=False, errMsg='path not exist.')
    try:
        os.makedirs(path+'/'+dirName)
        return jsonify(data=None, success=True, errMsg='')
    except Exception as e:
        return jsonify(data=None, success=False, errMsg=e)



@require_POST
@check_login
def fileUpload(request):
    """
    文件上传
    """
    upload_file = request.FILES.get("file")
    path = request.POST.get('path')
    if not upload_file:
        return jsonify(data=None, success=False, errMsg='未找到上传文件')
    if  not path or not os.path.exists(path):
        return jsonify(data=None, success=False, errMsg='未找到文件夹')
    
    new_file_path = path + '/' + upload_file.name
    try:
        #如果新文件存在则删除
        if os.path.exists(path + '/' + upload_file.name):
            try:
                os.remove(path + '/' + upload_file.name)
            except:
                pass
        content = upload_file.read()
        fp = open(new_file_path, 'wb')
        fp.write(content)
        fp.close()
        
        return jsonify(data=new_file_path, success=True, errMsg='')
    except:
        import traceback
        traceback.print_exc()
        return jsonify(data=None, success=False, errMsg='Upload file failed.')










