#coding=utf-8

import json
from django.http import HttpResponse

def jsonify(*args, **kwargs):
    if args and kwargs:
        raise TypeError('jsonify() behavior undefined when passed both args and kwargs')
    elif len(args) == 1:  # single args are passed directly to dumps()
        data = args[0]
    else:
        data = args or kwargs

    return HttpResponse(json.dumps(data), content_type='application/json')

def get_post_req_data(request):
    try:
        req_data = json.loads(request.body)
    except:
        return jsonify(data=None, success=False, errMsg='Request body format is incorrect.')
    return req_data
