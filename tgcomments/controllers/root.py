# -*- coding: utf-8 -*-
"""Main Controller"""
from tg import TGController
from tg import expose, flash, require, request, redirect, validate, config, hooks
from tg.i18n import ugettext as _, lazy_ugettext as l_

from tgcomments import model
from tgcomments.lib import get_user_gravatar, notify_comment_on_facebook,\
    make_fake_comment_entity, FakeCommentEntity, manager_permission

from tgext.pluggable import app_model, primary_key, instance_primary_key

from formencode.validators import Email, String, Invalid, Int
from tgext.datahelpers.utils import fail_with
from tg.predicates import not_anonymous
from datetime import datetime

try:
    from tgext.datahelpers.validators import MingEntityConverter as EntityConverter
except ImportError:
    from tgext.datahelpers.validators import SQLAEntityConverter as EntityConverter

import logging

log = logging.getLogger(__name__)


def _primary_key(type):
    pk = primary_key(type)
    try:
        return pk.name  # ming
    except AttributeError:
        return pk.key  # sqlalchemy


def back_to_referer(message=None, status=None, *args, **kw):
    if message:
        flash(message, status)
    if request.referer is not None:
        raise redirect(request.referer)
    raise redirect(request.host_url)


class RootController(TGController):
    def new_error_handler(self, *args, **kwargs):
        back_to_referer(l_('Please provide comment details'), 'error')

    @expose()
    @validate({'entity_type': String(not_empty=True),
               'entity_id': String(not_empty=True),
               'body': String(not_empty=True)},
              error_handler=new_error_handler)
    def new(self, **kw):
        entity_type = getattr(app_model, kw['entity_type'], None)
        entity_id = kw['entity_id']
        if entity_type is None or entity_id is None:
            return back_to_referer(_('Failed to post comment'), status='error')

        if issubclass(entity_type, FakeCommentEntity):
            entity = make_fake_comment_entity(entity_type, entity_id)
        else:
            entity = model.provider.get_obj(
                entity_type, {_primary_key(entity_type): entity_id})
            if not entity:
                return back_to_referer(_('Failed to post comment'), status='error')

        if not request.identity:
            try:
                user = {
                    'name': String(not_empty=True).to_python(kw.get('author')),
                    'avatar': get_user_gravatar(Email(not_empty=True).to_python(kw.get('email'))),
                    'user_name': 'anon',
                }
            except Invalid:
                return back_to_referer(_('A name and an email are required in order to comment'),
                                       status='error')
        else:
            user = request.identity['user']

        hooks.notify('tgcomments.before_add', args=(entity, user, kw))
        c = model.Comment.add_comment(entity, user, kw['body'])
        hooks.notify('tgcomments.after_add', args=(c,))
        notify_comment_on_facebook(request.referer, c)
        return back_to_referer(_('Comment Added'))

    @expose()
    @require(manager_permission())
    def delete(self, comment):
        primary_field = model.provider.get_primary_field(model.Comment)
        model.provider.delete(model.Comment, {primary_field: comment})
        return back_to_referer(_('Comment Deleted'))

    @expose()
    @require(manager_permission())
    @validate({'comment':EntityConverter(model.Comment)},
              error_handler=fail_with(404))
    def hide(self, comment):
        comment.hidden = not comment.hidden
        if comment.hidden:
            return back_to_referer(_('Comment Hidden'))
        return back_to_referer(_('Comment Displayed'))

    @expose()
    @require(not_anonymous())
    @validate({'comment':EntityConverter(model.Comment),
               'value':Int(not_empty=True)},
              error_handler=fail_with(404))
    def vote(self, comment, value):
        user = request.identity['user']
        user_votes = [vote for vote in comment.votes if vote.user_id == instance_primary_key(user)]
        vote = user_votes[0] if len(user_votes) != 0 else None

        min_vote_value, max_vote_value = config['_pluggable_tgcom'
            'ments_config'].get('votes_range', (-1, 1))
        value = min(max(min_vote_value, value), max_vote_value)

        if vote is None:
            try:
                vote = model.provider.create(model.CommentVote, dict(
                    comment_id=instance_primary_key(comment),
                    user_id=instance_primary_key(user),
                    created_at=datetime.utcnow(),
                    value=value,
                ))
            except Exception as e:
                log.error(e)
                return back_to_referer(_('Already voted this comment'), status='error')
        else:
            if vote.value != value:
                vote.value = value
                return back_to_referer(_('Vote updated'))
            else:
                return back_to_referer(_('Already voted this comment'), status='warning')
        return back_to_referer(_('Thanks for your vote!'))
