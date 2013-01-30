# -*- coding: utf-8 -*-

from os.path import join, dirname

from setuptools import setup, find_packages

from version import get_version

setup(
    name='media-hosts',
    version=get_version(),
    description='Gets media info from sites like Youtube and Soundcloud',
    author='Changaco',
    author_email='changaco ατ changaco δοτ net',
    url='https://github.com/Changaco/python-media-hosts',
    license='LGPLv3+',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    install_requires = [
        'miss>=0.2',
    ],
)
