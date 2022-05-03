# -*- coding: utf-8 -*-
from datetime import datetime
from hashlib import md5
from tg import url, config, request
import json
from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import urlopen
from contextlib import closing
from collections import namedtuple

def manager_permission():
    from tg.predicates import in_group, has_permission, Any
    return Any(in_group('tgcmanager'), has_permission('tgcomments-manage'))

def get_user_gravatar(user):
    if not isinstance(user, str):
        user = user.email_address
    mhash = md5(user.encode()).hexdigest()
    return url('http://www.gravatar.com/avatar/'+mhash, params=dict(s=32))

def _get_user_avatar(user):
    author_pic = getattr(user, 'avatar', None)
    if author_pic is None:
        author_pic = get_user_gravatar(user)
        fbauth = getattr(user, 'fbauth', None)
        if fbauth:
            author_pic = fbauth.profile_picture
    return author_pic

def get_user_avatar(user):
    return config['_pluggable_tgcomments_config'].get('get_user_avatar', _get_user_avatar)(user)

def notify_comment_on_facebook(url, comment):
    notify_faceook = config['_pluggable_tgcomments_config'].get('notify_facebook', True)
    if not notify_faceook:
        return

    user = comment.user
    if not user:
        return

    fbauth = getattr(user, 'fbauth', None)
    if not fbauth:
        return

    #check if facebook token has expired
    if not fbauth.access_token_expiry or datetime.now() >= fbauth.access_token_expiry:
        return

    fburl = 'https://graph.facebook.com/me/feed?access_token=%s' % fbauth.access_token
    data = {'link':url, 'message':comment.body.encode('utf-8')}
    with closing(urlopen(fburl, urlencode(data))) as fbanswer:
        return json.loads(fbanswer.read())

class FakeCommentEntity(object):
    class __mapper__(object):
        primary_key = [namedtuple('FakeColumn', ['key'])('uid')]

    def __init__(self, uid):
        self.uid = uid

def make_fake_comment_entity(entity_type, entity_id):
    fake_comment_type = type(entity_type.__name__, (FakeCommentEntity,), {})
    return fake_comment_type(entity_id)
