#!/usr/bin/env python
"""Script to generate info on duplicate files. This version is written in python (2.6+).
   Use help or docstrings to get more detailed documentation.

    Usage:
        dupfinder.py [-h] [-d SRCHLIST] [-e EXCLIST] [-c]
    Examples:
        dupfinder.py -d dir1 -d dir2 -d dir3 -e dir2_5  # standard mode
        dupfinder.py -d dir1 -d dir2 --column           # column mode
        dupfinder.py --gui                              # gui mode
"""

from dupfinder_core import DuplicateFinder as Dup
from dupfinder_wxtop import guimain # needed only for gui mode
import sys
import argparse
import re

DEBUG = False

# ------------------------------------------------------------------------- #
def main(args):
    """Argument Parser & caller"""

    parser = argparse.ArgumentParser(description="Duplicate Finder (CMD line)")

    parser.add_argument("-d", "--dir", dest='srchlist', action='append',
               help="Directories to search (can specify multiple times, twice for column mode)")
    parser.add_argument("-e", "--exclude", dest='exclist', action='append',
               help="Directories to exclude (can specify multiple times)")
    parser.add_argument("-c", "--column", default=False, action='store_true',
               help="Run in column mode. Note that -d should be specified exactly twice in this mode")
    parser.add_argument("-g", "--gui", default=False, action='store_true',
               help="Run in gui mode. Other options are not needed when gui mode is specified")

    parsed_args = parser.parse_args(args)

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

    if parsed_args.exclist:
        print 'INFO. directories to exclude:'
        for p in parsed_args.exclist: print ' ', p

    dup_obj = build_dupfinder(parsed_args.srchlist, parsed_args.exclist)
    print 'INFO. default matched dirs (relative) to exclude:'
    for p in dup_obj._ignorematching: print ' ', p

    if parsed_args.column:    # column mode
        print '\nINFO. column mode specified for directories "{}" vs "{}"'.format(
            parsed_args.srchlist[0], parsed_args.srchlist[1])
        colmode_srch(dup_obj)
    else:                     # standard mode
        print '\nINFO. dirs to search :'
        for p in parsed_args.srchlist: print ' ', p
        stdmode_srch(dup_obj)


# ------------------------------------------------------------------------- #
def build_dupfinder(srchlist, exclist=None):
    """Build DuplicateFinder
        srchlist:  list of directories to search
        exclist :  list of directories to exclude
    """

    print "** 1. Creating file/directory structure **"
    dup_obj = Dup.DuplicateFinder()

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
def stdmode_srch(dup_obj):
    """Std mode search of directories in duplicate object"""

    print "** 2. Finding duplicates (standard mode)**"
    #dup_table = dup_obj.get_duplicates()
    dup_obj.get_duplicates()

    print '-' * 70
    print "  Raw table { 'md5sum1' : [sz, file1, file2, file3, ...], ... }"
    print '-' * 70

    # NOTE. There is a big BUG in dump_duplicates(0) call!!
    # dup_obj.dump_duplicates(0)
    logs, sizes = dup_obj.dump_duplicates_list()
    for l in logs: print l

    #print '*' * 50     # for debug
    #print dup_table    # for debug


# ------------------------------------------------------------------------- #
def colmode_srch(dup_obj):
    """Column mode search of directories in duplicate object"""

    print "** 2. Finding duplicates (column mode)**"

    # start the more exhaustive search
    # data-structure conversion routine
    # ----------------------------------------
    root1 = dup_obj._root_dirlist[0]
    root2 = dup_obj._root_dirlist[1]

    # each of these will store a list of lists
    root1_list = []
    root2_list = []

    dup_table = dup_obj.get_duplicates()

    for flist in dup_table.values():
        # print "flist => ", flist - all files in list have same content
        flist.pop(0)
        flist1 =  []
        flist2 =  []
        for fname in flist:
            if re.search(r'/.svn', fname):       # skip ".svn" files
                continue
            #if re.search(r'/.git', fname):       # skip ".git" files
            #    continue
            if re.search(root1, fname):
                fname = re.sub(root1 + '/', '', fname)
                flist1.append(fname)
            if re.search(root2, fname):
                fname = re.sub(root2 + '/', '', fname)
                flist2.append(fname)

        # build a pair of lists fore each hashsum
        if (len(flist1) + len(flist2)) < 2:  # remove empty or single-elem lists
            continue
        root1_list.append( flist1 )
        root2_list.append( flist2 )

    # print "DIR1 LIST len", len(root1_list), root1_list
    # print "DIR2 LIST len", len(root2_list), root2_list

    # display routine
    # root1_list & root2_list have everything
    # -------------------------------------

    """
     prints in following format
     ======================
     root1     |    root2
     ======================
     file1     |    filea
     file2     |
               |
     file3     |    fileb
               |    filec
               |
     ======================
    """

    spc = ' ' * (40 - len(root1))
    print '=' * 90
    print root1, spc, " | \t", root2
    print '=' * 90
    for (flist1,flist2) in zip(root1_list,root2_list):
        # flist1 and flist2 contain lists of identical files
        # but flist1 files may not match flist2 files
        flist1 = sorted (flist1)
        flist2 = sorted (flist2)
        # the map operator puts in None for unequal length lists
        print " " * 40, "  | "
        # print "-" * 90
        for (f1,f2) in map(None, flist1,flist2):
            if (f1 == None): f1 = ' '
            if (f2 == None): f2 = ' '
            spc = ' ' * (40 - len(f1))
            print  f1 , spc,  " | \t", f2

    print " " * 40, "  | "
    print '=' * 90


if (__name__ == "__main__"):
    main(sys.argv[1:])
