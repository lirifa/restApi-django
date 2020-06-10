# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from utils.bases.models import BaseModel
from django.db import models

# Create your models here.
image_types_choices = (
    ('cover', '文章封面'),
    ('avatar', '头像'),
    ('other', '其他'),
)


class Image(BaseModel):
    name = models.CharField(max_length=64, verbose_name='图片名')
    type = models.CharField(choices=image_types_choices, default='other',max_length=32, verbose_name='图片类型')
    user = models.ForeignKey('user.User', verbose_name='所属用户')
    address = models.CharField(max_length=256, verbose_name='图片地址')

    class Meta(BaseModel.Meta):
        db_table = 'tb_image'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }

