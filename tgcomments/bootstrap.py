# -*- coding: utf-8 -*-
"""Setup the tgcomments application"""

from tgcomments import model
from tgext.pluggable import app_model

def bootstrap(command, conf, vars):
    print 'Bootstrapping tgcomments...'

    g = app_model.Group(group_name='tgcmanager', display_name='TGComments manager')
    model.DBSession.add(g)
    model.DBSession.flush()

    u1 = model.DBSession.query(app_model.User).filter_by(user_name='manager').first()
    if u1:
        g.users.append(u1)
    model.DBSession.flush()