#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='Youthmap',
    version='1.0',
    description='Youth movement',
    author='Adrian Fedoreanu',
    author_email='adrian.fedoreanu@gmail.com',
    url='http://me-phedoreanu.rhcloud.com/youthmap',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django_select2', 'MySQL-python==1.2.4', 'Django==1.5.5', 'django-crispy-forms==1.4.0',
                      'django-suit==0.2.5', 'South==0.8.2', 'pillow==2.2.1', 'django-cities-light==2.1.5',
                      'sorl-thumbnail==11.12', 'django-ratings==0.3.7'],
)
