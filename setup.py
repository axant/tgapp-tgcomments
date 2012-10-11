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
    'tgext.datahelpers >= 0.0.6'
]

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

setup(
    name='tgapp-tgcomments',
    version='0.0.4',
    description='TurboGears2 pluggable application for comments to entities with facebook sharing',
    long_description=README,
    author='Alessandro Molina',
    author_email='alessandro.molina@axant.it',
    url='https://bitbucket.org/_amol_/tgapp-tgcomments',
    keywords='turbogears2.application',
    setup_requires=["PasteScript >= 1.7"],
    paster_plugins=[],
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    package_data={'tgapp.tgcomments': ['i18n/*/LC_MESSAGES/*.mo',
                                 'templates/*/*',
                                 'public/*/*']},
    entry_points="""
    """,
    zip_safe=False
)
