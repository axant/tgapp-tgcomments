# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate, config
from tg.exceptions import HTTPForbidden, HTTPRedirection
from tg.i18n import ugettext as _, lazy_ugettext as l_

from tgcomments import model
from tgcomments.model import DBSession, Comment, CommentVote
from tgcomments.lib import get_user_gravatar, notify_comment_on_facebook, make_fake_comment_entity, FakeCommentEntity

try:
    from tg import predicates
except ImportError:
    from repoze.what import predicates

from tgext.pluggable import app_model

from formencode.validators import Email, String, Invalid, Int
from tgext.datahelpers.validators import SQLAEntityConverter
from tgext.datahelpers.utils import fail_with

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

        if issubclass(entity_type, FakeCommentEntity):
            entity = make_fake_comment_entity(entity_type, entity_id)
        else:
            entity = DBSession.query(entity_type).get(entity_id)
            if not entity:
                return back_to_referer()

        if not request.identity:
            try:
                user = {'name':String(not_empty=True).to_python(kw.get('author')),
                        'avatar':get_user_gravatar(Email(not_empty=True).to_python(kw.get('email')))}
            except Invalid:
                return back_to_referer()
        else:
            user = request.identity['user']

        c = Comment.add_comment(entity, user, kw['body'])
        notify_comment_on_facebook(request.referer, c)
        flash(_('Comment Added'))
        return back_to_referer(success=True)

    @expose()
    @require(predicates.in_group('tgcmanager'))
    @validate({'comment':SQLAEntityConverter(Comment)},
              error_handler=fail_with(404))
    def delete(self, comment):
        DBSession.delete(comment)
        flash(_('Comment Deleted'))
        return back_to_referer(success=True)

    @expose()
    @require(predicates.in_group('tgcmanager'))
    @validate({'comment':SQLAEntityConverter(Comment)},
              error_handler=fail_with(404))
    def hide(self, comment):
        comment.hidden = not comment.hidden
        if comment.hidden:
            flash(_('Comment Hidden'))
        else:
            flash(_('Comment Displayed'))
        return back_to_referer(success=True)

    @expose()
    @require(predicates.not_anonymous())
    @validate({'comment':SQLAEntityConverter(Comment),
               'value':Int(not_empty=True)},
              error_handler=fail_with(403))
    def vote(self, comment, value):
        user = request.identity['user']

        vote = DBSession.query(CommentVote).filter_by(comment=comment).filter_by(user=user).first()
        if not vote:
            vote = CommentVote(comment=comment, user=user)
            DBSession.add(vote)

        votes_range = config['_pluggable_tgcomments_config'].get('votes_range', (-1, 1))
        min_vote_value = votes_range[0]
        max_vote_value = votes_range[1]

        vote.value = min(max(min_vote_value, value), max_vote_value)
        flash(_('Thanks for your vote!'))
        return back_to_referer(success=True)

