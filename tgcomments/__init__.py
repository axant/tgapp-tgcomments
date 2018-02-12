# -*- coding: utf-8 -*-
"""The tgapp-tgcomments package"""

from tg.configuration import milestones

def plugme(app_config, options):
    from tgcomments import model
    milestones.config_ready.register(model.configure_models)
    app_config['_pluggable_tgcomments_config'] = options
    return dict(appid='tgcomments', global_helpers=False)
