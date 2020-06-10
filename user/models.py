# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from utils.bases.models import BaseModel

user_power_choices = (
    (0, '普通用户'),
    (1, '特约用户'),
    (2, '封禁用户'),
)


# Create your models here.
class User(BaseModel):
    """用户"""
    account = models.CharField(max_length=64, verbose_name='账号')
    password = models.CharField(max_length=64, verbose_name='密码')
    nickname = models.CharField(max_length=64, verbose_name='昵称')
    power = models.IntegerField(default=0, choices=user_power_choices, verbose_name='权限')
    email = models.EmailField(unique=True,verbose_name='头像')
    avatar = models.CharField(default='http://oss.iclould.xyz/avatar/admin.jpg',max_length=256, verbose_name='头像')

    class Meta(BaseModel.Meta):
        db_table = 'tb_user'
        verbose_name = verbose_name_plural = '用户'
    
    def __str__(self):
        return self.nickname

    def get_password(self):
        return '%s' %(self.password)

    def to_dict_detail(self):
        return {
                'id': self.id,
                'account': self.account,
                'nickname': self.nickname,
                'power': self.power,
                'avatar': self.avatar,
                'email': self.email,
                'create_dt': self.create_dt.strftime('%Y-%m-%d %H:%M:%S'),
                'last_dt': self.last_dt.strftime('%Y-%m-%d %H:%M:%S'),
            }

