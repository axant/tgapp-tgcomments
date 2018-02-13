# -*- coding: utf-8 -*-
"""Setup the tgcomments application"""

from tgcomments import model
from tgext.pluggable import app_model

import logging

log = logging.getLogger(__name__)


def bootstrap(command, conf, vars):
    log.info('Bootstrapping tgcomments...')

    p = app_model.Permission(
        permission_name='tgcomments-manage',
        description='Permits to manage comments',
    )

    g = app_model.Group(
        group_name='tgcmanager',
        display_name='TGComments manager'
    )

    try:
        model.DBSession.add(p)
        model.DBSession.add(g)
    except AttributeError:
        # mute ming complaints
        pass
    model.DBSession.flush()
