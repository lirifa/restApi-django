#-*- coding:utf-8 -*-
import os
import time
from datetime import datetime
from utils.constants import FILE_SAVE_PATH, OSS_URL


def save_upload_file(new_file_path, raw_file, name, param):
    """
    功能说明：保存上传文件
    raw_file:原始文件对象
    new_file_path:新文件绝对路径
    """
    try:
        # 如果新文件存在则删除
        if os.path.exists(new_file_path):
            try:
                os.remove(new_file_path)
            except:
                pass

        content = raw_file.read()
        fp = open(new_file_path, 'wb')
        fp.write(content)
        fp.close()
        return new_file_path.replace(FILE_SAVE_PATH, OSS_URL, 1)
    except Exception as e:
        print(e)
        return False

def save_block_file(block_file, param):
    """
    :param block_file: 文件对象
    :return:
    """
    # 唯一标识 + 文件名   201801171.png
    now_time = datetime.now().strftime("%Y%m%d%H%M%S")
    name = '%s_%s' % (now_time, block_file.name)
    block_file_path = get_absolute_file_path(name, param).replace("\\", "/")
    # 文件上传保存
    return save_upload_file(block_file_path, block_file, name, param)

def get_absolute_file_path(file_name, param):
    """
    功能说明：返回绝对路径字符串
    file_name:文件名字
    """
    date_dir = datetime.now().strftime("%Y%m%d")
    media_root = FILE_SAVE_PATH + '/' + param + '/' + date_dir
    absolute_file_path = os.path.join(media_root, file_name)
    print("absolute_file_path", absolute_file_path)
    # 返回文件绝对路径中目录路径
    file_dir = os.path.dirname(absolute_file_path)
    print("file_dir", file_dir)
    if not os.path.exists(file_dir):
        # 创建路径
        os.makedirs(file_dir)
    return absolute_file_path
