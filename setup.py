#!/usr/bin/env python2.7
# Run as: python setup.py install --user

#from distutils.core import setup   - DO NOT USE; DUMPS EVERTYHING UNDER SITE-PACKAGES & UNCLEAN INSTALL  

from setuptools import setup, find_packages

__version__ = '0.2.0'

setup(
    name = 'dupfinder',   
    version = __version__, 
    author = 'Mahmud Hassan',
    author_email = 'mhassan1900@users.noreply.github.com',
    description='Duplicate File Finder & Compare capability', 
    scripts = ['scripts/dupfinder', 'scripts/dupfinder_gui'],
    package_dir = {'': 'src'}, 
    #packages = find_packages(exclude=('testdir',)),
    py_modules = ['dupfinder', 'dupfinder_core.DuplicateFinder', 'dupfinder_core.hashsum', 
                  'dupfinder_wx.cmppanel', 'dupfinder_wx.mainpanel', 'dupfinder_wx.stdpanel', 'dupfinder_wxtop'] 
)

