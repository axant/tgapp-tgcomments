# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate
from tg.exceptions import HTTPForbidden, HTTPRedirection
from tg.i18n import ugettext as _, lazy_ugettext as l_

from tgcomments import model
from tgcomments.model import DBSession, Comment
from tgcomments.lib import get_user_gravatar, notify_comment_on_facebook

from tgext.pluggable import app_model

from formencode.validators import Email, String, Invalid

def back_to_referer(*args, **kw):
    if not kw.get('success'):
        flash('Failed to post comment', 'error')
    raise redirect(request.referer)

class RootController(TGController):
    @expose()
    @validate({'entity_type':String(not_empty=True),
               'entity_id':String(not_empty=True),
               'body':String(not_empty=True)},
              error_handler=back_to_referer)
    def new(self, **kw):
        entity_type = getattr(app_model, kw['entity_type'], None)
        entity_id = kw['entity_id']
        if entity_type is None or entity_id is None:
            return back_to_referer()

        entity = DBSession.query(entity_type).get(entity_id)
        if not entity:
            return back_to_referer()

        if not request.identity:
            try:
                user = {'name':String(not_empty=True).to_python(kw.get('author')),
                        'avatar':get_user_gravatar(Email(not_empty=True).to_python(kw.get('email')))}
            except Invalid, e:
                print e
                return back_to_referer()
        else:
            user = request.identity['user']

        c = Comment.add_comment(entity, user, kw['body'])
        notify_comment_on_facebook(request.referer, c)
        flash('Comment Added')
        return back_to_referer(success=True)

