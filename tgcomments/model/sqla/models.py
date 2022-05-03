from sqlalchemy.schema import Index
import tg

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, UnicodeText, Boolean, String
from sqlalchemy.orm import backref, relation
from tg.predicates import has_permission, in_group

from tgcomments.model import DeclarativeBase, DBSession
from tgcomments.lib import get_user_avatar
from tgext.pluggable import app_model, primary_key, instance_primary_key

from datetime import datetime


class Comment(DeclarativeBase):
    __tablename__ = 'tgcomments_comments'
    __table_args__ = (Index('idx_commented_entity', "entity_type", "entity_id"), )

    uid = Column(Integer, autoincrement=True, primary_key=True)

    body = Column(UnicodeText, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    hidden = Column(Boolean, default=False, nullable=False)

    user_id = Column(Integer, ForeignKey(primary_key(app_model.User)), nullable=True)
    user = relation(app_model.User, backref=backref('comments'))

    author_username = Column(Unicode(2048), default='anon')
    author_name = Column(Unicode(2048), nullable=False)
    author_pic = Column(Unicode(2048), nullable=True)

    entity_id = Column(Integer, nullable=False, index=True)
    entity_type = Column(Unicode(255), nullable=False, index=True)

    @property
    def voters(self):
        return DBSession.query(app_model.User).join(CommentVote).filter(CommentVote.comment_id==self.uid)

    @property
    def my_vote(self):
        values = [vote.value for vote in self.votes if vote.user_id == instance_primary_key(tg.request.identity['user'])]
        return values[0] if len(values) != 0 else None

    @property
    def rank(self):
        return sum((v.value for v in self.votes))

    def votes_by_value(self, v):
        return DBSession.query(CommentVote).filter_by(comment_id=self.uid).filter_by(value=v).all()

    @classmethod
    def get_entity_descriptor(cls, entity):
        Type = entity.__class__
        type_primary_key = primary_key(Type)
        return Type.__name__, getattr(entity, type_primary_key.key)

    @classmethod
    def comments_for(cls, entity, hidden='auto'):
        entity_type, entity_id = cls.get_entity_descriptor(entity)

        comments = DBSession.query(cls).filter_by(entity_type=entity_type)\
                                       .filter_by(entity_id=entity_id)

        if not (hidden==True or \
                (hidden=='auto' and tg.request.identity and cls.manager_permission())):
            comments = comments.filter_by(hidden=False)

        return comments.order_by(cls.created_at.desc()).all()


    @staticmethod
    def manager_permission():
        return in_group('tgcmanager') or has_permission('tgcmanager')

    @classmethod
    def add_comment(cls, entity, user, body):
        entity_type, entity_id = cls.get_entity_descriptor(entity)
        c = Comment(body=body, entity_type=entity_type, entity_id=entity_id)

        if isinstance(user, dict):
            c.author_username = user.get('user_name')
            c.author_name = user['name']
            c.author_pic = user.get('avatar')
        else:
            c.user = user
            c.author_username = user.user_name
            c.author_name = user.display_name
            c.author_pic = get_user_avatar(user)

        DBSession.add(c)
        return c


class CommentVote(DeclarativeBase):
    __tablename__ = 'tgcomments_comments_votes'
    __table_args__ = (Index('idx_comment_voter', "comment_id", "user_id", unique=True), )

    uid = Column(Integer, autoincrement=True, primary_key=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    value = Column(Integer, default=1)

    user_id = Column(Integer, ForeignKey(primary_key(app_model.User)), nullable=False)
    user = relation(app_model.User, backref=backref('comments_votes'))

    comment_id = Column(Integer, ForeignKey(Comment.uid), nullable=False)
    comment = relation(Comment, backref=backref('votes'))
