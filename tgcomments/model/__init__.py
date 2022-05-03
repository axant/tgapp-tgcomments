# -*- coding: utf-8 -*-
import tg
from tgext.pluggable import PluggableSession
import logging

log = logging.getLogger(__name__)

DBSession = PluggableSession()
DeclarativeBase = None
provider = None

Comment = None
CommentVote = None

def init_model(app_session):
    DBSession.configure(app_session)


def configure_models():
    global provider, Comment, CommentVote, DeclarativeBase

    if tg.config.get('use_sqlalchemy', False):
        log.info('Configuring TGComments for SQLAlchemy')
        from sqlalchemy.ext.declarative import declarative_base
        DeclarativeBase = declarative_base()
        from tgcomments.model.sqla.models import Comment, CommentVote
        from sprox.sa.provider import SAORMProvider
        provider = SAORMProvider(session=DBSession, engine=False)
    elif tg.config.get('use_ming', False):
        log.info('Configuring TGComments for Ming')
        from tgcomments.model.ming.models import Comment, CommentVote
        from sprox.mg.provider import MingProvider
        provider = MingProvider(DBSession)
    else:
        raise ValueError('TGComments should be used with sqlalchemy or ming')
