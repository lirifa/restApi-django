#coding=utf-8

import functools

from utils.helpers.jsonify import jsonify
from user.models import User

def post_check(content_type):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            request = args[0]
            if request.method == 'POST':
                if request.content_type != content_type:
                    return jsonify(data=None, success=False, errMsg='Content-type error.')

                account = request.META.get('HTTP_X_AC')
                rid = request.META.get('HTTP_X_RID')
                if not account and not rid:
                    return jsonify(data=None, success=False, errMsg='Lack of user info in request headers.')

            return func(*args, **kwargs)
        return wrapper
    return decorator
