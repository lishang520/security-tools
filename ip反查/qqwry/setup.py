#!/usr/bin/env python
import os
from setuptools import setup

def read_file(path):
    with open(os.path.join(os.path.dirname(__file__), path), encoding='utf-8-sig') as fp:
        return fp.read()

setup(
    name='qqwry-py3',
    version='1.2.1',
    description='Lookup location of IP in qqwry.dat, for Python 3.0+',
    long_description=read_file('README.rst'),
    long_description_content_type='text/x-rst',
    author='Ma Lin',
    author_email='malincns@163.com',
    url='https://github.com/animalize/qqwry-python3',
    license='BSD',
    keywords = 'qqwry cz88 纯真 ip归属地',
    platforms=['any'],
    package_dir={'qqwry': 'qqwry'},
    py_modules=['qqwry.__init__', 'qqwry.qqwry', 'qqwry.cz88update'],
    packages=['qqwry'],
    package_data={"qqwry": ['py.typed']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities'
    ]
)
