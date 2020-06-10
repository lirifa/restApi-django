#-*- coding:utf-8 -*-

import os
import time
from datetime import datetime
from PIL import Image
from utils.constants import FILE_SAVE_PATH
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

IMAGE_FORMATS = {
    "JPEG" : "jpg",
    "JPG" : "jpg",
    "PNG" : "png",
    "GIF" : "gif",
}

class BaseImage(object):
    def __init__(self, image_format):
        self._image_format = image_format
        self._filename = "%s/%s" % (self.build_dirpath(),
            self.build_filename(IMAGE_FORMATS[self._image_format]))

    def get_size(self):
        raise NotImplementedError

    def get_filename(self):
        return self._filename

    def save(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def build_dirpath(self):
        return datetime.now().strftime("%Y/%m/%d")

    def build_filename(self, image_format):
        return "%s.%s" % (int(time.time() * 1000000), image_format)

    def base64decode(self, image_content):
        return base64_decode(image_content)


class LocalImage(BaseImage):
    def __init__(self, image_file):
        _dir = self.build_dirpath()
        self._local_path = FILE_SAVE_PATH
        image_save_abspath = "%s/%s" % (self._local_path, _dir)
        if not os.path.exists(image_save_abspath):
            os.makedirs(image_save_abspath)
        self._sio = image_file
        self._image = Image.open(self._sio)
        self._width, self._heigth = self._image.size
        super(LocalImage, self).__init__(self._image.format)

    def get_size(self):
        return (float(self._width), float(self._heigth))

    def save(self):
        self._sio.seek(0)
        self._sio.save(os.path.join(self._local_path, self._filename))

    def close(self):
        self._image.close()
        self._sio.close()

ImageStorage = LocalImage


def rescale_image(buf):
    """活动、攻略等封面图裁剪"""
    W, H = 900, 540

    image_file = StringIO(buf)
    image = Image.open(image_file)
    w, h = image.size

    if float(w)/h > float(W)/H:# 宽高比大于W/H，按高缩放再裁剪宽度
        image = image.resize((int(w*float(H)/h), H), Image.ANTIALIAS)
        w, h = image.size
        cut = (w-W)/2
        region = (cut, 0, w-cut, h)
        image = image.crop(region)
    else:# 宽高比小于W/H，按宽缩放再裁剪高度
        image = image.resize((W, int(h*float(W)/w)), Image.ANTIALIAS)
        w, h = image.size
        cut = (h-H)/2
        region = (0, cut, w, h-cut)
        image = image.crop(region)

    image_file = StringIO()
    image.save(image_file, 'JPEG', quality=100)
    return image_file

def rescale_headphoto(buf):
    """头像裁剪，比例1:1"""
    image_file = StringIO(buf)
    image = Image.open(image_file)
    w, h = image.size
    
    image = image.resize((min(w,h), min(w, h)), Image.ANTIALIAS)

    image_file = StringIO()
    image.save(image_file, 'JPEG', quality=100)
    return image_file

