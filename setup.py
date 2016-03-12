# coding=utf-8
from setuptools import setup, find_packages
from codecs import open
from os import path

import targetprocess

here = path.abspath(path.dirname(__file__))
VERSION = targetprocess.__version__

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='targetprocess-client',
    version=VERSION,
    description='Python library to help getting data from TargetProcess API',
    long_description=long_description,
    url='https://github.com/magicjohnson/targetprocess-client',
    download_url='https://github.com/magicjohnson/targetprocess-client/archive/v{}.zip'.format(VERSION),
    author='Dmitriy Trochshenko',
    author_email='dmitriy.trochshenko@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='targetprocess api',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pytz',
        'requests',
        'six',
    ],
)
