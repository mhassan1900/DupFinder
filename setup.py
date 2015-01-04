#!/usr/bin/env python2.7
# Run as:
# python setup.py install --user

#from distutils.core import setup   - DO NOT USE; DUMPS EVERTYHING UNDER SITE-PACKAGES & UNCLEAN INSTALL  

# packages=['DupFinder'],               # don't work

from setuptools import setup, find_packages

setup(name='dupfinder_wx',   # best to have same names as main source file
      # author='Mahmud Hassan',
      # author_email='mahmud.hassan@gmail.com',
      version='1.0.0',
      description='Duplicate File Finder',
      package_dir = {'': 'src'}, # /dupfinder_wx'},     
      # packages = find_packages(exclude=('testdir',)),
      packages = ['dupfinder_wx'],
      scripts = ['scripts/dupfinder_gui', 'scripts/dupfinder'],
      py_modules=['DuplicateFinder', 'hashsum'],
                # 'find_duplicates_wxgui' , 'find_duplicates_tkgui']  # These are really scripts
)
