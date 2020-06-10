#coding=utf-8

import base64
import rc4

from user.models import User
from utils.helpers.jsonify import jsonify
from utils.constants import GAME_KEY

def current_user(request):
    account = request.META.get('HTTP_X_AC')
    rid = request.META.get('HTTP_X_RID')

    try:
        if account:
            account = base64.b64decode(account)
            account = rc4.rc4(account, GAME_KEY)
            user = User.objects.filter(account=account).first()
        elif rid:
            rid = base64.b64decode(rid)
            rid = rc4.rc4(rid, GAME_KEY)
            user = User.objects.filter(rid=rid).first()
        else:
            return jsonify(data=None, success=False, errMsg='Lack of user info.')
    except:
        return jsonify(data=None, success=False, errMsg='User info decode error.')

    if not user:
        return jsonify(data=None, success=False, errMsg="User is not logined.")
    return user
