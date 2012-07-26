# -*- coding: utf-8 -*-
"""Setup the tgcomments application"""

from tgcomments import model
from tgext.pluggable import app_model

def bootstrap(command, conf, vars):
    print 'Bootstrapping tgcomments...'
