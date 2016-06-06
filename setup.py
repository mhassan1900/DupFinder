#!/usr/bin/env python2.7
# Run as: python setup.py install --user

#from distutils.core import setup   - DO NOT USE; DUMPS EVERTYHING UNDER SITE-PACKAGES & UNCLEAN INSTALL

import sys
from setuptools import setup, find_packages

# Shenanighans to deal with dirs without __init__.py 
sys.path.insert(0, 'src')
from version import __version__
sys.path = sys.path[1:]

setup(
    name = 'dupfinder',
    version = __version__,
    author = 'Mahmud Hassan',
    author_email = 'mhassan1900@users.noreply.github.com',
    description='Duplicate File Finder & Compare capability',
    scripts = ['scripts/dupfinder', 'scripts/dupfinder_gui'],
    package_dir = {'': 'src'},
    #packages = find_packages(exclude=('testdir',)),
    py_modules = ['dupfinder', 'dupfinder_core.DuplicateFinder', 'dupfinder_core.hashsum', 'version',
                  'dupfinder_wx.cmppanel', 'dupfinder_wx.mainpanel', 'dupfinder_wx.stdpanel', 'dupfinder_wxtop']
)
