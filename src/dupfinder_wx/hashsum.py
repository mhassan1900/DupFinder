##########################################################################
# File:     hashsum.py
# Version:  0.20
# Author:   Mahmud Hassan
# Date:     Jan 2016
# License:  Lesser GPL ... 
# Summary:  Wrapper functions for hashlib to generate hash sums on 
#           filenames.This version just uses the python supplied 'hashlib' 
#           library to return the sums for md5, sha1, sha224, sha256, 
#           sha384 and sha512. 
##########################################################################

import hashlib 
import os.path
"""Wrapper functions for hashlib to generate hash sums on filenames"""

_DEFAULT_CHUNK_ = 4096 # bytes

_hashrefs_ = {
   'md5':    hashlib.md5   ,
   'sha1':   hashlib.sha1  ,
   'sha224': hashlib.sha224,
   'sha256': hashlib.sha256,
   'sha384': hashlib.sha384,
   'sha512': hashlib.sha512
}


def md5sum (fname, chunksize=_DEFAULT_CHUNK_): 
    """Computes md5 sum of input filename using hashlib library
    Example: md5sum( filename )       - reads entire file into memory
             md5sum( filename, 4096 ) - reads 4096 bytes at a time"""

    fin = _hashsum_fopen(fname)
    hashsum = hashlib.md5()
    for contents in iter(lambda: fin.read(chunksize), b''): 
        hashsum.update (contents) 

    fin.close() 
    return hashsum.hexdigest()  



def sha1sum (fname, chunksize=_DEFAULT_CHUNK_):
    """Computes sha1 sum of input filename using hashlib library
    Example: shah1sum( filename )       - reads entire file into memory
             shah1sum( filename, 4096 ) - reads 4096 bytes at a time"""

    fin = _hashsum_fopen(fname)
    hashsum = hashlib.sha1()
    for contents in iter(lambda: fin.read(chunksize), b''): 
        hashsum.update (contents) 

    fin.close() 
    return hashsum.hexdigest()  



def sha224sum (fname, chunksize=_DEFAULT_CHUNK_):
    """Computes sha224 sum of input filename using hashlib library
    Example: shah224sum( filename )       - reads entire file into memory
             shah224sum( filename, 4096 ) - reads 4096 bytes at a time"""

    fin = _hashsum_fopen(fname)
    hashsum = hashlib.sha224()
    for contents in iter(lambda: fin.read(chunksize), b''): 
        hashsum.update (contents) 

    fin.close() 
    return hashsum.hexdigest()  



def sha256sum (fname, chunksize=_DEFAULT_CHUNK_):
    """Computes sha256 sum of input filename using hashlib library
    Example: shah256sum( filename )       - reads entire file into memory
             shah256sum( filename, 4096 ) - reads 4096 bytes at a time"""

    fin = _hashsum_fopen(fname)
    hashsum = hashlib.sha256()
    for contents in iter(lambda: fin.read(chunksize), b''): 
        hashsum.update (contents) 

    fin.close() 
    return hashsum.hexdigest()  



def sha384sum (fname, chunksize=_DEFAULT_CHUNK_):
    """Computes sha384 sum of input filename using hashlib library
    Example: shah384sum( filename )       - reads entire file into memory
             shah384sum( filename, 4096 ) - reads 4096 bytes at a time"""

    fin = _hashsum_fopen(fname)
    hashsum = hashlib.sha384()
    for contents in iter(lambda: fin.read(chunksize), b''): 
        hashsum.update (contents) 

    fin.close() 
    return hashsum.hexdigest()  



def sha512sum (fname, chunksize=_DEFAULT_CHUNK_):
    """Computes sha512 sum of input filename using hashlib library
    Example: shah512sum( filename )       - reads entire file into memory
             shah512sum( filename, 4096 ) - reads 4096 bytes at a time"""

    fin = _hashsum_fopen(fname)
    hashsum = hashlib.sha512()
    for contents in iter(lambda: fin.read(chunksize), b''): 
        hashsum.update (contents) 

    fin.close() 
    return hashsum.hexdigest()  



def _hashsum_fopen(fname):
    """Just performs error checking on file open before returning fileid"""
    try:
        fid = open (fname, 'rb')
    except:
        print 'Something wrong with file' , fname 
        exit() 

    return fid 



# ------------------------------------------------------------------------ #
# Advanced calls - generic wrappers                                        #
# ------------------------------------------------------------------------ #
def gen_hashsum(fname, hashtype="md5", chunksize=_DEFAULT_CHUNK_): 
    """Computes hashsum based on hashtype
    Example: gen_hashsum( filename )               - returns md5 hashsum
             gen_hashsum( filename, 'sha1' )       - returns sha1 hashsum
             gen_hashsum( filename, 'sha1', 4096 ) - returns sha1 hashsum 
                                                     reading 4k bytes at a time
    """
    fin = _hashsum_fopen(fname)
    hsum = _hashrefs_[hashtype]() 
    for contents in iter(lambda: fin.read(chunksize), b''): 
        hsum.update (contents) 
    fin.close() 
    return hsum.hexdigest()  



def gen_partial_hashsum(fname, hashtype, chunksize, offset=0): 
    """Generates partial hashsum on filename based on hashtype for specific chunksize
    with an offset from head (or tail < 0). Generally allowed to overshoot when giving chunksize > filesize. 
    However, negative offset magnitude must not exceed filesize in bytes else will return error (None).

    Example: gen_partial_hashsum( filename, 'sha1', 2048 )        - returns sha1 hashsum on first 2k bytes
             gen_partial_hashsum( filename, 'sha1', 4096, -4096 ) - returns sha1 hashsum on last 4k bytes

    if filename has size 67,239 bytes then, the following are equivalent (full file hashsum)
            gen_hashsum( filename ) 
            gen_partial_hashsum( filename, 'md5', 67239 ) 
            gen_partial_hashsum( filename, 'md5', 80000 ) 
            gen_partial_hashsum( filename, 'md5', 80000, -67239 ) 

    Following hashsums for first 4096 bytes are equivalent: 
            gen_partial_hashsum( filename, 'md5', 4096 ) 
            gen_partial_hashsum( filename, 'md5', 4096, -67239 ) 

    Following hashsums for last 4096 bytes are equivalent: 
            gen_partial_hashsum( filename, 'md5', 4096, (67239-4096) ) 
            gen_partial_hashsum( filename, 'md5', 5000, (67239-4096) ) 
            gen_partial_hashsum( filename, 'md5', 4096, -4096)  
            gen_partial_hashsum( filename, 'md5', 5000, -4096)  
    
    Following generates an error (IOError exception) and returns None: 
            gen_partial_hashsum( filename, 'md5', 4096, -80000 )   # negative offset > file size
    """
    fin = _hashsum_fopen(fname)
    hsum = _hashrefs_[hashtype]()

    try:
        if offset < 0:
            fin.seek(offset, 2) 
        else:
            fin.seek(offset) 
    except:
        print 'ERROR. Could not perform fileseek by specified offset {}'.format(offset)
        fin.close()
        return None

    contents = fin.read(chunksize)
    hsum.update (contents) 
    fin.close() 
    return hsum.hexdigest()  




def gen_partial_hashsums_safe(fname, hashtype="md5", chunksize=_DEFAULT_CHUNK_):
    """Generates 3 partial hashsum on file given filename, hashtype and optionally a chunksize.
    Hashsums are on first, middle and last "chunks" of the file.

    Returns: head_hsum, middle_hsum, tail_hsum (tuple of 3 strings)

    Example: gen_partial_hashsums(filename)               - returns 3 md5  hashsums on 4k byte chunks 
             gen_partial_hashsums(filename, 'sha1')       - returns 3 sha1 hashsums on 4k byte chunks
             gen_partial_hashsums(filename, 'sha1', 8192) - returns 3 sha1 hashsums on 8k byte chunks

    NOTE. If chunksize > filesize, will just generate and return a 3-tuple of the same hashsum 
    """


    fsize = os.path.getsize(fname)

    if chunksize > fsize:
        hsum = gen_hashsum(fname, hashtype, chunksize)
        return hsum, hsum, hsum

    fin = _hashsum_fopen(fname)

    hsum1 = _hashrefs_[hashtype]()
    hsum2 = _hashrefs_[hashtype]()
    hsum3 = _hashrefs_[hashtype]()

    contents1 = fin.read(chunksize) # head portion
    hsum1.update (contents1)     

    fin.seek((fsize-chunksize)/2)
    contents2 = fin.read(chunksize) # middle portion
    hsum2.update (contents2)     

    fin.seek(-chunksize, 2)
    contents3 = fin.read(chunksize) # tail portion
    hsum3.update (contents3)     

    fin.close() 
    return hsum1.hexdigest(), hsum2.hexdigest(), hsum3.hexdigest() 



def gen_partial_hashsums(fname, hashtype="md5", chunksize=_DEFAULT_CHUNK_, fsize=None):
    """Generates 3 partial hashsum on file given filesize, filename, hashtype and optionally a chunksize.
    Hashsums are on first, middle and last "chunks" of the file.

    Returns: head_hsum, middle_hsum, tail_hsum (tuple of 3 strings)

    Example: gen_partial_hashsums(67239, filename)               - returns 3 md5  hashsums on 4k byte chunks 
             gen_partial_hashsums(67239, filename, 'sha1')       - returns 3 sha1 hashsums on 4k byte chunks
             gen_partial_hashsums(67239, filename, 'sha1', 8192) - returns 3 sha1 hashsums on 8k byte chunks

    NOTE. If chunksize > filesize, will just generate and return a 3-tuple of the same hashsum 
    """

    fin = _hashsum_fopen(fname)

    if fsize==None:
        fsize = os.path.getsize(fname)

    if chunksize > fsize:
        hsum = gen_hashsum(fname, hashtype, chunksize)
        return hsum, hsum, hsum

    hsum1 = _hashrefs_[hashtype]()
    hsum2 = _hashrefs_[hashtype]()
    hsum3 = _hashrefs_[hashtype]()

    contents1 = fin.read(chunksize) # head portion
    hsum1.update (contents1)     

    fin.seek((fsize-chunksize)/2)
    contents2 = fin.read(chunksize) # middle portion
    hsum2.update (contents2)     

    fin.seek(-chunksize, 2)
    contents3 = fin.read(chunksize) # tail portion
    hsum3.update (contents3)     

    fin.close() 
    return hsum1.hexdigest(), hsum2.hexdigest(), hsum3.hexdigest() 




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
        # print "md5sum => ", md5sum2(fname)


