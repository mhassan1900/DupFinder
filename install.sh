#!/bin/bash -f
/bin/rm -rf  ./dist ./build
# pip uninstall DuplicateFinder 
python2.7 ./setup.py install --user

