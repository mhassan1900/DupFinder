#!/usr/bin/env python
#pylint: disable=fixme
#pylint: disable=too-many-locals

"""
This module is responsible for displaying duplicates in an appropriate manner.
It serves as the presentation layer. Standard search display is easy but column mode
display requires enough work to warrant its own space.
"""


import os.path as osp

DEBUG = False

# ------------------------------------------------------------------------- #
def stdmode_srch(dup_obj):
    """Std mode search of directories in duplicate object"""

    print "** 2. Finding duplicates (standard mode)**"
    dup_obj.get_duplicates()

    print '-' * 70
    print "  Raw table { 'md5sum1' : [sz, file1, file2, file3, ...], ... }"
    print '-' * 70

    # NOTE. There is a big BUG in dump_duplicates(0) call!!
    logs, _ = dup_obj.dump_duplicates_list()
    for l in logs: print l


# ------------------------------------------------------------------------- #
def colmode_srch(dup_obj):
    """Column mode search of directories in duplicate object. Displays
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

    print "** 2. Finding duplicates (column mode)**"

    root1 = dup_obj._root_dirlist[0] #pylint: disable=W0212
    root2 = dup_obj._root_dirlist[1] #pylint: disable=W0212
    absroot1, absroot2 = osp.abspath(root1), osp.abspath(root2)
    dup_table = dup_obj.get_duplicates() # already skips matching duplicates

    # each of these will store a list of lists
    root1_list, root2_list = [], []

    _matches_rootdir = lambda f, d: f.startswith(d)
    maxlen = len(root1)
    root2len = max(40, len(root2))

    for flist in dup_table.values():
        flist.pop(0)
        flist1, flist2 = [], []
        for fname in flist:     # fname should be full (abs)path
            if _matches_rootdir(fname, absroot1):
                fsuffix = fname.replace(absroot1, '')
                flist1.append(fsuffix[1:])
                if len(fsuffix[1:]) > maxlen: maxlen = len(fsuffix[1:])
            elif _matches_rootdir(fname, absroot2): # superfluous step for safety
                fsuffix = fname.replace(absroot2, '')
                flist2.append(fsuffix[1:])
            else:
                print 'WARNING. Cannot place {} in either {} or {}'.format(fname,root1,root2)
                continue
        # build a pair of lists fore each hashsum
        if (len(flist1) + len(flist2)) < 2:  # remove empty or single-elem lists
            continue
        root1_list.append( flist1 )
        root2_list.append( flist2 )


    # display routine - root1_list & root2_list have everything
    linelen = maxlen + root2len + 3
    print '=' * linelen
    print '{0:{1}s} | {2:}'.format(root1, maxlen, root2)
    print '=' * linelen
    i = 0
    for (flist1,flist2) in zip(root1_list,root2_list):
        # flist1 and flist2 contain lists of identical files
        # but flist1 files may not match flist2 files
        flist1 = sorted (flist1)
        flist2 = sorted (flist2)
        # the map operator puts in None for unequal length lists
        for (f1,f2) in map(None, flist1,flist2):
            if (f1 == None): f1 = ' '
            if (f2 == None): f2 = ' '
            print  '{0:{1}s} | {2:}'.format(f1, maxlen, f2)
        i += 1
        if i < len(root1_list):
            print '-' * maxlen, '+', '-'* root2len
    print '=' * linelen
