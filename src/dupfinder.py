#!/usr/bin/env python
#pylint: disable=fixme
#pylint: disable=too-many-locals

"""Script to generate info on duplicate files. This version is written in python (2.6+).
   Use help or docstrings to get more detailed documentation.

    Usage:
        dupfinder [-h] [-d SEARCHDIR] [-e EXCLUDEDIR] [-p IGNOREPATTERN] [-c] [-g] [-v]
    Examples:
        dupfinder -d dir1 -d dir2 -d dir3 -e dir2_5  # standard mode
        dupfinder -d dir1 -d dir2 --column           # column mode
        dupfinder --gui                              # gui mode
        dupfinder -d dir1 -e dir1_5 -p '*.pyc'       # exclude file patterns (not implemented)
"""


import logging
import sys
import argparse

from dupfinder_core import DuplicateFinder
from dupfinder_core import dupdisp
from dupfinder_wxtop import guimain # needed only for gui mode
from version import __version__

DEBUG = False
_log = logging.getLogger(__name__)

# ------------------------------------------------------------------------- #
#TODO. Implement ignorepatlist
def build_dupfinder(srchlist, exclist=None, ignorepatlist=None):  #pylint: disable=unused-argument
    """Initialization of DuplicateFinder object to prepare for search
        srchlist     :  list of directories to search
        exclist      :  list of directories to exclude
        ignorepatlist:  list of file patterns to exclude

        Returns: a DuplicateFinder object properly initialized, ready for search
    """

    print "** 1. Creating file/directory structure **"
    dup_obj = DuplicateFinder.DuplicateFinder()

    if exclist != None:
        for mypath in exclist:
            dup_obj.add2ignore(mypath)
            print "      Ignoring: ", mypath

    for mypath in srchlist:
        dup_obj.update(mypath)
        print "      Building structure for: ", mypath

    if (DEBUG): dup_obj.dump_files()
    print "-- Directory structure creation complete --\n"
    return dup_obj


# ------------------------------------------------------------------------- #
def main(args):
    """Argument Parser & caller"""

    parser = argparse.ArgumentParser(description="Duplicate Finder (CMD line)")

    parser.add_argument("-d", "--dir", dest='srchlist', action='append',
               help="Directories to search (can specify multiple times, twice for column mode)")
    parser.add_argument("-e", "--exclude", dest='exclist', action='append',
               help="Directories to exclude (can specify multiple times)")
    parser.add_argument("-p", "--ignorepat", dest='ignorepatlist', action='append',
               help="Patterns to exclude (can specify multiple times)")
    parser.add_argument("-c", "--column", default=False, action='store_true',
               help="Run in column mode. Note that -d should be specified exactly twice in this mode")
    parser.add_argument("-g", "--gui", default=False, action='store_true',
               help="Run in gui mode. Other options are not needed when gui mode is specified")
    parser.add_argument("-v", "--version", dest='version', default=False, action='store_true',
               help="Prints out the version of dupfinder")

    parsed_args = parser.parse_args(args)

    if parsed_args.version:
        print 'DupFinder Version', __version__
        return

    if parsed_args.gui:         # gui mode
        guimain()
        return

    if parsed_args.srchlist==None:  # soft error condition
        print '\nNo directory list specified; nothing to report. Exiting.\n'
        parser.print_help()
        return
    elif len(parsed_args.srchlist)!=2 and parsed_args.column: # error condition
        print "ERROR. Column mode must have only 2 directories!"
        parser.print_help()
        return

    if parsed_args.ignorepatlist:
        print 'WARNING. This is unsupported at the moment. Will have no effect!!!'
        print 'INFO. patterns to exclude:'
        for p in parsed_args.ignorepatlist: print ' ', p

    if parsed_args.exclist:
        print 'INFO. directories to exclude:'
        for p in parsed_args.exclist: print ' ', p

    dup_obj = build_dupfinder(parsed_args.srchlist, parsed_args.exclist)
    print 'INFO. default matched names to exclude:'
    for p in dup_obj._ignorematching: print ' ', p

    if parsed_args.column:    # column mode
        print '\nINFO. column mode specified for directories "{}" vs "{}"'.format(
            parsed_args.srchlist[0], parsed_args.srchlist[1])
        dupdisp.colmode_srch(dup_obj)
    else:                     # standard mode
        print '\nINFO. dirs to search :'
        for p in parsed_args.srchlist: print ' ', p
        dupdisp.stdmode_srch(dup_obj)




if (__name__ == "__main__"):
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])
