#coding=utf-8

import base64
import json
from functools import wraps
from django.http import JsonResponse
from user.models import User

def check_post(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.method == 'POST':
            if request.content_type != 'application/json':
                return JsonResponse({'data': None, 'success': False, 'errMsg': 'Content-type error.'})
            if request.body:
                try:
                    request.POST = json.loads(request.body)
                except:
                    return JsonResponse({'data': None, 'success': False, 'errMsg': 'Request body format error.'})
        return view_func(request, *args, **kwargs)
    return wrapped_view


def check_login(func): 
    """
    查看session值用来判断用户是否已经登录
    :param func:
    :return:
    """
    def warpper(request,*args,**kwargs):
        if request.session.get('user_id'):
            return func(request, *args, **kwargs)
        else:
            return JsonResponse({'data': None, 'code': 'nologin', 'success': False, 'errMsg': '用户未登陆'})
    
    return warpper
