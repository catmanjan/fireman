#!/usr/bin/env python

from distutils.core import setup

setup(name='Fireman',
      version='1.0',
      description='Firewall Manager',
      author='Michael Ko',
      author_email='u5010095@anu.edu.au',
      url='https://github.com/catmanjan/fireman',
      packages=['src', 'src/core', 'src/rte', 'src/services', 'src/utils'],
      package_data={'src/core': ['master.conf']},
     )