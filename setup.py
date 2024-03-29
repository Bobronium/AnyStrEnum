
# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import os.path

readme = ''
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.rst')
if os.path.exists(readme_path):
    with open(readme_path, 'rb') as stream:
        readme = stream.read().decode('utf8')


setup(
    long_description=readme,
    name='AnyStrEnum',
    version='0.2.0',
    description='Elegant implementation of Enum which inherits from str or bytes',
    python_requires='>=3.6',
    author='MrMrRobat',
    author_email='appkiller16@gmail.com',
    license='MIT',
    keywords='enum str strenum bytesenum bytestrenum typing auto autoenum',
    classifiers=['Development Status :: 4 - Beta', 'Intended Audience :: Developers',
                 'Intended Audience :: System Administrators', 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.7',
                 'Topic :: Software Development :: Libraries :: Python Modules'],
    packages=['anystrenum'],
    package_data={},
    install_requires=[],
    extras_require={'inflection': ['inflection'], 'tests': ['pytest'], 'dev': ['pytest']},
)
