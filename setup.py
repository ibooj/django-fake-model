#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import django_fake_model

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = django_fake_model.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

if sys.argv[-1] == 'gen_travis':
    with open('.travis_tmp.yml', 'r') as tmp:
        template = ''.join(tmp.readlines())
    python_versions = ('py26', 'py27', 'py32', 'py33', 'py34', 'py35')
    django_versions = ('16', '17', '18', 'master')
    db_versions = ('sqlite', 'postgres', 'mysql')
    filter_envs = (lambda x: not (x[0] == 'py26' and x[1] != '16'))
    versions = list(filter(filter_envs, [(py, dj, db) for py in python_versions
                                                      for dj in django_versions
                                                      for db in db_versions]))
    allow_failure = (lambda x: x[1] == 'master' or x[0] == 'py35' or
                               (x[2] == 'mysql' and x[0] == 'py32' and x[1] in ['18', '17', '16']))
    env_tpl = '    - TOX_ENV={0}-dj{1}-{2}'
    envs = '\n'.join(map(lambda x: env_tpl.format(*x), versions))
    failure_tpl = '    - env: TOX_ENV={0}-dj{1}-{2}'
    failures = '\n'.join(map(lambda x: failure_tpl.format(*x), filter(allow_failure, versions)))
    with open('.travis.yml', 'w') as result:
        result.write(template.format(envs, failures))
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-fake-model',
    version=version,
    description="""Simple library for creating fake models in the unit tests.""",
    long_description=readme + '\n\n' + history,
    author='Kirill Ermolov',
    author_email='erm0l0v@ya.ru',
    url='https://github.com/erm0l0v/django-fake-model',
    packages=[
        'django_fake_model',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-fake-model',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
