from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm.declarative import MappedClass
from tgcomments import model
from tgext.pluggable import app_model, primary_key, instance_primary_key
from tg.predicates import has_permission, in_group
from tgcomments.lib import get_user_avatar, manager_permission
from datetime import datetime
import tg


class Comment(MappedClass):
    class __mongometa__:
        session = model.DBSession
        name = 'tgcomments_comments'
        indexes = [('entity_type', 'entity_id', )]

    _id = FieldProperty(s.ObjectId)

    body = FieldProperty(s.String, required=True)
    created_at = FieldProperty(s.DateTime, if_missing=datetime.now)
    hidden = FieldProperty(s.Bool, if_missing=False)

    user_id = ForeignIdProperty(app_model.User)
    user = RelationProperty(app_model.User)

    author_username = FieldProperty(s.String, if_missing='anon')
    author_name = FieldProperty(s.String, if_missing='Anonymous')
    author_pic = FieldProperty(s.String, if_missing='')

    entity_id = FieldProperty(s.ObjectId, required=True)
    entity_type = FieldProperty(s.String, required=True)

    @property
    def votes(self):
        return model.provider.query(CommentVote, filters={'comment_id': self._id})[1]

    @property
    def voters(self):
        return [vote.user for vote in self.votes]

    @property
    def my_vote(self):
        values = [vote.value for vote in self.votes if vote.user_id == instance_primary_key(tg.request.identity['user'])]
        return values[0] if len(values) != 0 else None

    @property
    def rank(self):
        return sum((v.value for v in self.votes))

    def votes_by_value(self, v):
        return [vote for vote in self.votes if vote.value == v]

    @classmethod
    def get_entity_descriptor(cls, entity):
        Type = entity.__class__
        type_primary_key = primary_key(Type)
        return Type.__name__, getattr(entity, type_primary_key.name)

    @classmethod
    def comments_for(cls, entity, hidden='auto'):
        entity_type, entity_id = cls.get_entity_descriptor(entity)

        comments = model.provider.query(cls, filters={'entity_type': entity_type,
                                                 'entity_id': entity_id})[1]

        if not (hidden == True or (hidden == 'auto' and manager_permission())):
            comments = (comment for comment in comments if not comment.hidden)

        return sorted(comments, key=lambda c: c.created_at, reverse=True)

    @classmethod
    def add_comment(cls, entity, user, body):
        entity_type, entity_id = cls.get_entity_descriptor(entity)

        c = dict(body=body, entity_type=entity_type, entity_id=entity_id)
        if isinstance(user, dict):
            c['author_username'] = user['user_name']
            c['author_name'] = user['name']
            c['author_pic'] = user.get('avatar')
        else:
            c['user_id'] = instance_primary_key(user)
            c['user'] = user
            c['author_username'] = user.user_name
            c['author_name'] = user.display_name
            c['author_pic'] = get_user_avatar(user)

        return model.provider.create(cls, c)


class CommentVote(MappedClass):
    class __mongometa__:
        session = model.DBSession
        name = 'tgcomments_comments_votes'
        unique_indexes = [("_id", "comment_id", "user_id", )]

    _id = FieldProperty(s.ObjectId)

    created_at = FieldProperty(s.DateTime, if_missing=datetime.now, required=True)
    value = FieldProperty(s.Int, if_missing=1)

    user_id = FieldProperty(s.ObjectId)
    user = ForeignIdProperty(app_model.User)

    comment_id = FieldProperty(s.ObjectId)
    comment = ForeignIdProperty(Comment)
