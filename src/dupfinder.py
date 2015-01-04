#!/usr/bin/env python
"""
##########################################################################
# File:     dupfinder.py 
# Version:  0.10
# Author:   Mahmud Hassan
# Date:     July 2011
# License:  Lesser GPL ... 
# Summary:  Script to generate info on duplicate files
#           This version is written in python (2.6+), so help or 
#           docstrings can be used to get more detailed documentation. 
##########################################################################

Usage: 
        dupfinder.py <dir1> ... <dirN> [option] #  batch mode 
        dupfinder.py                            #  interactive mode  

        [option] must be one of -help or -column

"""


from dupfinder_wx.DuplicateFinder import DuplicateFinder 
import sys
import argparse
import re

DEBUG = False



def main2(args):
    """Argument Parser & caller"""

    parser = argparse.ArgumentParser(description="Duplicate Finder (CMD line)") 

    parser.add_argument("-d", "--dir", dest='srchlist', action='append',
               help="Directories to search (can specify multiple times, twice for column mode)") 
    parser.add_argument("-e", "--exclude", dest='exclist', action='append', 
               help="Directories to exclude (can specify multiple times)") 
    parser.add_argument("-c", "--column", default=False, action='store_true', 
               help="Run in column mode. Note usage of -d options should be exactly twice in this mode") 

    parsed_args = parser.parse_args(args)

    # -- print some info --
    if not parsed_args.srchlist: parsed_args.srchlist = []
    if not parsed_args.exclist: parsed_args.exclist = []

    print 'INFO. dirs to search :'
    for p in parsed_args.srchlist: print p
    print 'INFO. dirs to exclude:'
    for p in parsed_args.exclist: print p
    print 'INFO. column mode    :', parsed_args.column



    if len(parsed_args.srchlist)==0: 
        print '\nNo directory list specified; nothing to report. Exiting.\n'
        return

    # build data struct
    dup_obj = build_dupfinder(parsed_args.srchlist, parsed_args.exclist)

    print 'INFO. matched dirs (relative) to exclude:',
    print dup_obj._ignorematching

    if parsed_args.column and len(dup_obj._root_dirlist) != 2:
        print "ERROR. Column mode must have only 2 roots!" 
        print parser.format_help()
        return


    # search
    if parsed_args.column:
        colmode_srch(dup_obj)
    else:
        stdmode_srch(dup_obj)




def build_dupfinder(srchlist, exclist=[]):
    """Build DuplicateFinder
        srchlist:  list of directories to search
        exclist :  list of directories to exclude 
    """

    # initialize & then update
    # ------------------------
    print "** 1. Creating file/directory structure **" 

    dup_obj = DuplicateFinder() 

    for mypath in exclist:
       dup_obj.add2ignore(mypath) 
       print "      Ignoring: ", mypath

    for mypath in srchlist:
       dup_obj.update(mypath) 
       print "      Building structure for: ", mypath

    if (DEBUG): dup_obj.dump()
    print "-- Directory structure creation complete --\n"

    return dup_obj



def stdmode_srch(dup_obj):
    """Std mode search of directories in duplicate object"""

    # report duplicates
    # -----------------
    print "** 2. Finding duplicates **"

    dup_table = dup_obj.get_duplicates()

    print '-' * 70
    print "  Raw table { 'md5sum1' : [sz, file1, file2, file3, ...], ... }"  
    print '-' * 70

    # NOTE. There is a big BUG in dump_duplicates(0) call!!
    # dup_obj.dump_duplicates(0)  
    logs, sizes = dup_obj.dump_duplicates_list()
    for l in logs: print l
    
    #print '*' * 50     # for debug
    #print dup_table    # for debug



def colmode_srch(dup_obj):
    """Column mode search of directories in duplicate object"""

    # report duplicates
    # -----------------
    print "** 2. Finding duplicates **"


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
        sz = flist.pop(0) 
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
   #main()   
   main2(sys.argv[1:])   
   

