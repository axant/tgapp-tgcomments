# -*- coding: utf-8 -*-

"""WebHelpers used in tgapp-tgcomments."""

from tgcomments.lib import get_user_avatar, manager_permission
from tgext.pluggable import instance_primary_key


def upvoted_or_downvoted(comment):
    if not comment.my_vote:
        return ''
    return 'upvoted' if comment.my_vote > 0 else 'downvoted'
