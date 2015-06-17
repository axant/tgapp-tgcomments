About tgcomments
-------------------------

tgcomments is a Pluggable Comments application for TurboGears2.
Comments can be added to any webpage by using the ``comments_for`` partial.

TGComments supports Facebook for avatar if the user logged using tgapp-fbauth
or if the User model provides a similar interface. Otherwise will fallback to
Gravatar.

Installing
-------------------------------

tgcomments can be installed both from pypi or from bitbucket::

    pip install tgapp-tgcomments

should just work for most of the users

Plugging tgcomments
----------------------------

In your application *config/app_cfg.py* import **plug**::

    from tgext.pluggable import plug

Then at the *end of the file* call plug with tgcomments::

    plug(base_config, 'tgcomments')


To expose comments support for an entity, just call 
the ``comments_for(entity)``  partial for 
that entity inside your templates as explained in the 
**Exposed Partials** section.

Exposed Partials
----------------------

tgcomments exposes a bunch of partials which can be used
to render pieces of the blogging system anywhere in your
application:

- ``tgcomments.partials:comments_for(entity)``
    Given any SQLAlchemy entity which is available inside your application ``model`` module
    it will display a list of comments for that entity with a box to add a new comment.

Provided Options
--------------------

tgcomments supports a bunch of options that can be passed to the plug call
to change its behavior:

- *notify_facebook* (default:True) automatically notify on facebook comments that
    the user wrote if he has logged using Facebook
- *allow_anonymous* (default:True) allow anonymous users to comment

Exposed Templates
--------------------

The templates used by registration and that can be replaced with
*tgext.pluggable.replace_template* are:

- ``tgcomments.templates.comments_partial``
