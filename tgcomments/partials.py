from tg import expose, config
from tgcomments import model

@expose('tgcomments.templates.comments_partial')
def comments_for(entity):
    comments = model.Comment.comments_for(entity)
    allow_anonymous = config['_pluggable_tgcomments_config'].get('allow_anonymous', True)
    entity_type, entity_id = model.Comment.get_entity_descriptor(entity)
    return dict(entity_type=entity_type, entity_id=entity_id,
                comments=comments, allow_anonymous=allow_anonymous)
