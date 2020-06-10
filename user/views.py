# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from utils.helpers.jsonify import jsonify, get_post_req_data
from utils.helpers.decorators import check_post, check_login
from .models import User
import json
from django.core import serializers

@require_POST
@check_post
def adminLogin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user_obj = authenticate(username=username, password=password)
    if user_obj:
        auth_login(request, user_obj)
        return jsonify(data=None, success=True, errMsg='操作成功')
    else:
        return jsonify(data=None, success=False, errMsg='登录失败')


# 用户登录
@require_POST
@check_post
def login(req):
    account = req.POST.get('account')
    password = req.POST.get('password')
    if not account or not password:
        return jsonify(data=None, success=False, errMsg='缺少请求参数.')

    user = User.objects.get(account=account)
    user_password = user.get_password()
    userInfo = user.to_dict_detail()
    if  user is None:
        return jsonify(data=None, success=False, errMsg='用户名不存在！')
    elif password != user_password:
        return jsonify(data=None, success=False, errMsg='密码错误')
    else:
        req.session['user_id'] = userInfo['id']
        return jsonify(data=userInfo, success=True, errMsg='操作成功')

# 用户信息拉取
@require_POST
@check_login
def userInfo(req):
    id = req.session.get('user_id', default=None)
    if not id:
        return jsonify(data=None, code='nologin', success=False, errMsg='缺少请求参数.')
    
    user = User.objects.get(id=id)
    userInfo = user.to_dict_detail()
    return jsonify(data=userInfo, success=True, errMsg='操作成功')

# 用户信息更新
@require_POST
@check_post
@check_login
def updateInfo(req):
    nickname = req.POST.get('nickname')
    email = req.POST.get('email')
    try:
        user_id = req.session.get('user_id')
        email_exit = User.objects.exclude(id=user_id).filter(email=email)
        if email_exit.exists():
            return jsonify(data=None, success=False, errMsg='用户邮箱已存在')
        user = User.objects.get(id=user_id)
        user.nickname = nickname
        user.email = email
        user.save()
        return jsonify(data=None, success=True, errMsg='操作成功')
    except:
        return jsonify(data=None, success=False, errMsg='更新失败')


# 用户登出
@require_POST
def logout(req):
    try:
        req.session.flush()
    except KeyError:
        pass
    return jsonify(data=None, success=True, errMsg='操作成功')

