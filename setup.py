#! /usr/bin/env python

from setuptools import setup

setup(
    # http://pythonhosted.org/setuptools/setuptools.html
    name='smsframework-clickatell',
    version='0.0.2-2',
    author='Mark Vartanyan',
    author_email='kolypto@gmail.com',

    url='https://github.com/kolypto/py-smsframework-clickatell',
    license='MIT',
    description="SMS framework: Clickatell provider",
    long_description=open('README.rst').read(),
    keywords=['sms', 'message', 'notification', 'receive', 'send', 'clickatell'],

    packages=['smsframework_clickatell'],
    scripts=[],

    install_requires=[
        'smsframework >= 0.0.1',
    ],
    extras_require={
        'receiver': [  # sms receiving
            'flask >= 0.10',
        ],
        '_dev': ['wheel', 'nose', 'flask'],
    },
    test_suite='nose.collector',
    include_package_data=True,

    platforms='any',
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
)
