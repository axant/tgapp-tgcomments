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
    Given any SQLAlchemy or Ming entity (instance) which is available inside your application ``model`` module
    it will display a list of comments for that entity with a box to add a new comment.

Provided Options
--------------------

tgcomments supports a bunch of options that can be passed to the plug call
to change its behavior:

- *notify_facebook* (default:True) automatically notify on facebook comments that
    the user wrote if he has logged using Facebook
- *allow_anonymous* (default:True) allow anonymous users to comment

- *pretty_date* a function that will be used to properly format dates (example: "5 minutes ago")

- *get_user_avatar* a function that will be used to get the avatar (by default searches
for the ``avatar`` property, then fallbacks for fb information, then fallbacks gravatar)

Exposed Templates
--------------------

The templates used by registration and that can be replaced with
*tgext.pluggable.replace_template* are:

- ``tgcomments.templates.comments_partial``

Available Hooks
-------------
TGComments exposes some hooks to configure it's behavior, The hooks that can be
used with TurboGears2 register_hook are:

- ``tgcomments.before_add(entity, user, kw)`` - called before adding a comment. kw['body'] can be modified here


Changelog
---------

- ``0.2.3`` - added ``tgcomments.before_add`` hook
- ``0.2.2`` - fixed anon comment creation broken by v0.2.1, used pre instead of div to
    display the comment body, so it keeps newlines
- ``0.2.1`` - fixed ming relation with User and added author_username
- ``0.2.0`` - introduced compatibility with ming
