# -*- coding: utf-8 -*-

"""WebHelpers used in tgapp-tgcomments."""

from tgcomments.lib import get_user_avatar, manager_permission
from tgext.pluggable import instance_primary_key


def upvoted_or_downvoted(comment):
    from tg import request
    if not request.identity or not comment.my_vote:
        return ''
    return 'upvoted' if comment.my_vote > 0 else 'downvoted'


def _pretty_date(date_to_format):
    from datetime import datetime, timedelta
    from tg.i18n import lazy_ugettext
    now = datetime.utcnow()
    if date_to_format <= (now - timedelta(hours=24)):
        return date_to_format.strftime("%d/%m/%Y %H:%M")
    else:
        diff = now - date_to_format
        days, seconds = diff.days, diff.seconds
        minutes = (seconds % 3600) // 60
        hours = days * 24 + seconds // 3600
        if hours > 0:
            return lazy_ugettext('%s hours ago' % hours)
        return lazy_ugettext('%s minutes ago' % minutes)


def pretty_date(date):
    from tg import config
    return config['_pluggable_tgcomments_config'].get('pretty_date', _pretty_date)(date)
