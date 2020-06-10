# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from utils.helpers.jsonify import jsonify, get_post_req_data
from utils.helpers.decorators import check_post, check_login
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from .models import Article, Platform
from user.models import User

# Create your views here.
@check_login
@check_post
def create(req):
    """
    新建文章
    """
    title = req.POST.get('title')
    summary = req.POST.get('summary')
    content = req.POST.get('content')
    cover_url = req.POST.get('cover_url')
    status = req.POST.get('status')
    platforms = req.POST.get('platforms')
    
    try:
        user = User.objects.get(id = req.session.get('user_id'))
        article_obj = Article.objects.create(title=title, summary=summary, content=content, cover_url=cover_url,user=user)
        for platform in platforms:
            platform_obj = Platform.objects.filter(key=platform)
            article_obj.platform.add(*platform_obj)
        return jsonify(data=None, success=True, errMsg='操作成功')
    except:
        return jsonify(data=None, success=False, errMsg='创建文章失败')

@check_login
@check_post
def update(req):
    """ 
    编辑文章
    """
    article_id = req.POST.get('id')
    title = req.POST.get('title')
    summary = req.POST.get('summary')
    content = req.POST.get('content')
    cover_url = req.POST.get('cover_url')
    status = req.POST.get('status')
    if not article_id:
        return jsonify(data=None, success=False, errMsg='param error.')
    try:
        article_obj = Article.objects.get(id=article_id)
        article_obj.title = title
        article_obj.summary = summary
        article_obj.content = content
        article_obj.cover_url = cover_url
        article_obj.status = status
        article_obj.save()
        return jsonify(data=None, success=True, errMsg='文章修改成功')
    except:
        return jsonify(data=None, success=False, errMsg='文章修改失败')
                                                                                                                                

@require_GET
def articleDetail(req):
    """
    查看文章详情
    """
    articleId = req.GET.get('id')
    if not articleId:
        return jsonify(data=None, success=False, errMsg='param error.')
    try:
        article_obj = Article.objects.get(id=articleId)
        article_obj.reads_count += 1
        article_obj.save()
        return jsonify(data=article_obj.to_detail(), success=True, errMsg='操作成功')
    except Exception as e:
        return jsonify(data=None, success=False, errMsg=str(e))
         

@check_login
@check_post
def updateIsTop(req):
    """
    修改文章置顶
    """
    articleId = req.POST.get('id')
    isTop = req.POST.get('isTop')
    if not articleId or not isinstance(isTop, bool):
        return jsonify(data=None, success=False, errMsg='param error.')
    try:
        article_obj = Article.objects.get(id=articleId)
        article_obj.is_top = isTop
        article_obj.save()
        return jsonify(data=None, success=True, errMsg='操作成功')
    except:
        return jsonify(data=None, success=False, errMsg='置顶操作失败')

@require_GET
def fetchTopArticle(req):
    """
    获取置顶文章列表
    """
    top_articles = Article.objects.filter(is_top=True, status='published').order_by('-create_dt')
    data = [e.to_dict() for e in top_articles]
    return jsonify(data=data, success=True, errMsg='操作成功')

    try:
        top_articles = Article.objects.filter(is_top=True)
        data = [e.to_dict() for e in top_articles]
        return jsonify(data=data, success=True, errMsg='操作成功')
    except:
         return jsonify(data=None, success=False, errMsg='获取置顶文章失败')


@require_GET
def platformList(req):
    """
    获取全部平台列表
    """
    try:
        platforms = Platform.objects.all()
        json_list = []
        for platform in platforms:
            json_dict = {}
            json_dict['key'] = platform.key
            json_dict['name'] = platform.name
            json_list.append(json_dict)
        return jsonify(data=json_list, success=True, errMsg='操作成功')
    except:
        return jsonify(data=None, success=False, errMsg='获取平台信息失败')


@require_GET
def list(req):
    """
    获取文章列表
    """
    page = int(req.GET.get('page',1))
    limit = int(req.GET.get('limit', 10))
    try:
        article_list = Article.objects.filter(status='published').order_by('-create_dt')[(page-1)*limit :page*limit]
        data = {}
        data['list'] = [e.to_list() for e in article_list]
        data['total'] = Article.objects.filter(status='published').count()
        return jsonify(data=data, success=True, errMsg='操作成功')
    except:
        return jsonify(data=None, success=False, errMsg='查询失败')



@check_login
@require_GET
def allList(req):
    """
    获取全部文章列表
    """
    status = req.GET.get('status', None)
    page = int(req.GET.get('page',1))
    limit = int(req.GET.get('limit', 10))
    try:
        if not status:
            article_list = Article.objects.all().order_by('-create_dt')[(page-1)*limit :page*limit]
        else:
            article_list = Article.objects.filter(status=status).order_by('-create_dt')[(page-1)*limit :page*limit]
        data = {}
        data['list'] = [e.to_dict() for e in article_list]
        data['total'] = Article.objects.all().count()
        return jsonify(data=data, success=True, errMsg='操作成功')
    except:
        return jsonify(data=None, success=False, errMsg='查询失败')

