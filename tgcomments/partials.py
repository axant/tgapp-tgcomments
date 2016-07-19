from tg import expose, config
from tgcomments.model import Comment

@expose('tgcomments.templates.comments_partial')
def comments_for(entity):
    comments = Comment.comments_for(entity)
    allow_anonymous = config['_pluggable_tgcomments_config'].get('allow_anonymous', True)
    entity_type, entity_id = Comment.get_entity_descriptor(entity)
    return dict(entity_type=entity_type, entity_id=entity_id,
                comments=comments, allow_anonymous=allow_anonymous)