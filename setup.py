#!/usr/bin/env python3
from distutils.core import setup

setup(
    name='pysubrenamer',
    description='Rename subtitles files with the \
        same video filename',
    author='Alex Left',
    author_email='alejandro.izquierdo.b@gmail.com',
    url='https://github.com/alex-left/pysubrenamer',
    version=pysubrenamer.__version__,
    scripts=['pysubrenamer'],
    license='GPL-v3',
    long_description=open('README.md').read(),
)
