##########################################################################
# File:     hashsum.py
# Version:  0.10
# Author:   Mahmud Hassan
# Date:     July 2011
# License:  Lesser GPL ... 
# Summary:  Wrapper functions for hashlib to generate hash sums on 
#           filenames.This version just uses the python supplied 'hashlib' 
#           library to return the sums for md5, sha1, sha224, sha256, 
#           sha384 and sha512. 
##########################################################################

import hashlib 
"""Wrapper functions for hashlib to generate hash sums on filenames"""


def _hashsum_fopen(fname):
    """Just performs error checking on file open before returning fileid"""
    try:
        fid = open (fname, 'rb')
    except:
        print 'Something wrong with file' , fname 
        exit() 

    return fid 



def md5sum (fname): 
    """Computes md5 sum of input filename using hashlib library
    Example: md5sum( filename ) """

    fin = _hashsum_fopen(fname)
    hashsum = hashlib.md5()
    for contents in fin:
        hashsum.update (contents) 

    fin.close() 
    return hashsum.hexdigest()  



def sha1sum (fname):
    """Computes sha1 sum of input filename using hashlib library
    Example: sha1sum( filename ) """

    fin = _hashsum_fopen(fname)
    hashsum = hashlib.sha1()
    for contents in fin:
        hashsum.update (contents) 

    fin.close() 
    return hashsum.hexdigest()  



def sha224sum (fname):
    """Computes sha224 sum of input filename using hashlib library
    Example: sha224sum( filename ) """

    fin = _hashsum_fopen(fname)
    hashsum = hashlib.sha224()
    for contents in fin:
        hashsum.update (contents) 

    fin.close() 
    return hashsum.hexdigest()  



def sha256sum (fname): 
    """Computes sha256 sum of input filename using hashlib library
    Example: sha256sum( filename ) """

    fin = _hashsum_fopen(fname)
    hashsum = hashlib.sha256()
    for contents in fin:
        hashsum.update (contents) 

    fin.close() 
    return hashsum.hexdigest()  



def sha384sum (fname): 
    """Computes sha384 sum of input filename using hashlib library
    Example: sha384sum( filename ) """

    fin = _hashsum_fopen(fname)
    hashsum = hashlib.sha384()
    for contents in fin:
        hashsum.update (contents) 

    fin.close() 
    return hashsum.hexdigest()  



def sha512sum (fname): 
    """Computes sha512 sum of input filename using hashlib library
    Example: sha512sum( filename ) """

    fin = _hashsum_fopen(fname)
    hashsum = hashlib.sha512()
    for contents in fin:
        hashsum.update (contents) 

    fin.close() 
    return hashsum.hexdigest()  




############### test env ############### 

if (__name__ == "__main__"):
    import sys 

    imode = False 
    if imode:
        # interactive mode
        print "testing md5 sum -- " , "enter file name: "
        fname = raw_input()
        print "md5sum => ", md5sum(fname)
    else:
        print "no of args ", len(sys.argv)
        if (len(sys.argv) < 2): 
            print "No file entered... exiting"
            exit()

        print "testing md5 sum on file : ", sys.argv[1]
        fname = sys.argv[1]
        # batch mode
        print "md5sum => ", md5sum(fname)


