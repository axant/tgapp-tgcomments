# -*- coding: utf-8 -*-
import sys, os

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

install_requires=[
    "TurboGears2 >= 2.1.4",
    "tgext.pluggable",
    "tgext.datahelpers >= 0.0.6",
    "six",
]

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

setup(
    name='tgapp-tgcomments',
    version='0.2.6',
    description='TurboGears2 pluggable application for comments to entities with facebook sharing',
    long_description=README,
    author='Alessandro Molina, Vincenzo Castiglia',
    author_email='alessandro.molina@axant.it, vincenzo.castiglia@axant.it',
    url='https://github.com/axant/tgapp-tgcomments',
    keywords='turbogears2.application',
    setup_requires=[],
    paster_plugins=[],
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    package_data={'tgapp.tgcomments': ['i18n/*/LC_MESSAGES/*.mo',
                                 'templates/*/*',
                                 'public/*/*']},
    message_extractors={'tgcomments': [
        ('**.py', 'python', None),
        ('templates/**.xhtml', 'kajiki', None),
        ('public/**', 'ignore', None),
    ]},
    entry_points="""
    """,
    zip_safe=False
)
