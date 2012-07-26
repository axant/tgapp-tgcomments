# -*- coding: utf-8 -*-
"""The tgapp-tgcomments package"""

def plugme(app_config, options):
    app_config['_pluggable_tgcomments_config'] = options
    return dict(appid='tgcomments', global_helpers=False)