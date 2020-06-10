# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_dt = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    class Meta:
        abstract = True
        ordering = ['-create_dt', ]
