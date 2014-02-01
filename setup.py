#!/usr/bin/env python
"""
Flask-SSC
-----------

Adds a simple thread safe cache to flask

"""

from setuptools import setup

setup(
    name='Flask-SSC',
    version='0.1',
    url='http://github.com/Crowdlink/SimpleSafeCache',
    license='MIT',
    author='Isaac Cook',
    author_email='isaac@crowdlink.io',
    description='Adds thread safe in memeory cache support to your Flask application',
    long_description=__doc__,
    packages=[
        'flask_ssc',
    ],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    test_suite='test_ssc',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
