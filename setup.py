# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

classifiers = (
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 2.7',
#    'Programming Language :: Python :: 3.2',
#    'Programming Language :: Python :: 3.3',
    'License :: OSI Approved :: BSD License',
)

kw = {
    'name': 'cstitch',
    'version': '0.1',
    'description': 'Auto-generate Python ctypes interfaces using libclang',
    'long_description': open('README.rst', 'rt').read(),
    'author': 'Dan Miller',
    'author_email': 'dnmiller@gmail.com',
    'license': 'BSD License',
    'url': 'https://github.com/dnmiller/cstitch',
    'keywords': '',
    'classifiers': classifiers,
    'packages': ['cstitch'],
    'package_data': {'cstitch': ['*.html']},
    'install_requires': None,
    'zip_safe': True,
}

setup(**kw)
