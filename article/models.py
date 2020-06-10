# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from utils.bases.models import BaseModel
from tinymce.models import HTMLField

post_tag_type_choices = (
    (0, '普通标签'),
    (1, '推荐标签'),
)

# 文章状态，draft:草稿 published:已发布
article_status_choices = (
    ('draft', '草稿'),
    ('published', '已发布'),
)

# 文章状态，draft:草稿 published:已发布
article_type_choices = (
    ('html', '富文本'),
    ('markdown', 'Markdown'),
)



# Create your models here.
class Article(BaseModel):
    title = models.CharField(max_length=64, verbose_name='标题')
    content = HTMLField(null=True, blank=True, verbose_name='正文')
    content_type = models.CharField(max_length=32,choices=article_type_choices, default='html', verbose_name='文章格式类型')
    summary = models.CharField(max_length=256, null=True, verbose_name='摘要')
    user = models.ForeignKey('user.User', verbose_name='所属用户')
    cover_url = models.CharField(max_length=128, null=True, verbose_name='封面')
    reads_count = models.IntegerField(default=0, verbose_name='阅读量')
    status = models.CharField(max_length=32, choices=article_status_choices, default='draft', verbose_name='状态')
    is_top = models.BooleanField(default=False, verbose_name='置顶')
    comment_disabled = models.BooleanField(default=False, verbose_name='评论开关')
    reads_count = models.IntegerField(default=0, verbose_name='阅读量')
    like_count = models.IntegerField(default=0, verbose_name='喜欢量')
    tags = models.ManyToManyField('ArticleTag', blank=True, verbose_name='标签')
    platform = models.ManyToManyField('Platform', blank=True, verbose_name='终端')

    class Meta(BaseModel.Meta):
        db_table = 'tb_article'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'status': self.status,
            'status_name': dict(article_status_choices)[self.status],
            'reads_count': self.reads_count,
            'like_count': self.like_count,
            'is_top': self.is_top,
            'cover_url': self.cover_url,
        }
   

    def to_list(self):
        return {
            'id': self.id,
            'title': self.title,
            'cover_url': self.cover_url,
            'reads_count': self.reads_count,
            'like_count': self.like_count,
            'create_dt': self.create_dt.strftime('%Y-%m-%d %H:%I:%S'),
        }            


    def to_detail(self):
        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'content': self.content,
            'content_type': self.content_type,
            'status': self.status,
            'comment_disabled': self.comment_disabled,
            'cover_url': self.cover_url,
            'author': str(self.user),
            'create_dt': self.create_dt.strftime('%Y-%m-%d %H:%I:%S'),
        }


class ArticleTag(BaseModel):
    """文章标签"""
    name = models.CharField(max_length=64, unique=True, verbose_name='名称')
    type = models.IntegerField(choices=post_tag_type_choices, verbose_name='类别')# 0为普通标签 1为推荐标签

    class Meta(BaseModel.Meta):
        db_table = 'tb_articletag'
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

class Platform(BaseModel):
    """发布平台"""
    key = models.CharField(max_length=64, unique=True, verbose_name='平台关键字')
    name = models.CharField(max_length=64, verbose_name='平台名称')
    class Meta(BaseModel.Meta):
        db_table = 'tb_platform'

    def __str__(self):
         return self.name

    def to_dict(self):
        return {
            'key': self.key,
            'name': self.name,
        }
