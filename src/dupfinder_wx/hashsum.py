"""Wrapper functions for hashlib to generate hash sums on filenames"""

import sys
import hashlib
import os.path

DEFAULT_CHUNK = 2**18 # 256K bytes
SMALL_CHUNK = 1024    # 1K byte

# -------------------------------------------------------------------------- #
def _hashsum_fopen(fname):
    """Just performs error checking on file open before returning fileid"""
    try:
        fid = open (fname, 'rb')
    except:
        print 'Something wrong with file' , fname
        return None
    return fid

# -------------------------------------------------------------------------- #
def gen_hashsum(fname, hashtype="md5", chunksize=DEFAULT_CHUNK):
    """Computes hashsum based on hashtype
    Supports hashtype=[md5|sha1|sha224|sha256|sha256|sha384]
    Example: gen_hashsum( filename )               - returns md5 hashsum
             gen_hashsum( filename, 'sha1' )       - returns sha1 hashsum
             gen_hashsum( filename, 'sha1', 4096 ) - returns sha1 hashsum
                                                     reading 4k bytes at a time
    """
    fin = _hashsum_fopen(fname)
    hsum = getattr(hashlib, hashtype)()  # eg:  hashlib.md5()
    for contents in iter(lambda: fin.read(chunksize), b''):
        hsum.update (contents)
    fin.close()
    return hsum.hexdigest()

# ------------------------------------------------------------------------ #
# Advanced calls - generic wrappers                                        #
# ------------------------------------------------------------------------ #
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
    hsum = getattr(hashlib, hashtype)()

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


# -------------------------------------------------------------------------- #
def gen_partial_hashsums(fname, hashtype="md5", chunksize=SMALL_CHUNK, fsize=None):
    """Generates 3 partial hashsum on file given filesize, filename, hashtype and optionally a chunksize.
    Hashsums are on first, middle and last "chunks" of the file.

    Returns: head_hsum, middle_hsum, tail_hsum (tuple of 3 strings)

    Example: gen_partial_hashsums(67239, filename)               - returns 3 md5  hashsums on 4k byte chunks
             gen_partial_hashsums(67239, filename, 'sha1')       - returns 3 sha1 hashsums on 4k byte chunks
             gen_partial_hashsums(67239, filename, 'sha1', 8192) - returns 3 sha1 hashsums on 8k byte chunks

    NOTE. If chunksize > filesize, will just generate and return a 3-tuple of the same hashsum
    """

    if fsize==None:
        fsize = os.path.getsize(fname)

    if chunksize > fsize:
        #print 'thhis is too small - direct', fname
        hsum = gen_hashsum(fname, hashtype, chunksize)
        return hsum, hsum, hsum

    fin = _hashsum_fopen(fname)     # head portion
    contents1 = fin.read(chunksize)
    fin.seek((fsize-chunksize)/2)   # middle portion
    contents2 = fin.read(chunksize)
    fin.seek(-chunksize, 2)         # tail portion
    contents3 = fin.read(chunksize)

    hsum1 = getattr(hashlib, hashtype)(contents1)
    hsum2 = getattr(hashlib, hashtype)(contents2)
    hsum3 = getattr(hashlib, hashtype)(contents3)
    fin.close()
    return hsum1.hexdigest(), hsum2.hexdigest(), hsum3.hexdigest()


# -------------------------------------------------------------------------- #
# TEST ENV
# -------------------------------------------------------------------------- #
def main():
    imode = False
    if imode: # interactive mode
        print "testing md5 sum -- " , "enter file name: "
        fname = raw_input()
        print "md5sum => ", gen_hashsum(fname, 'md5')
    else:
        if (len(sys.argv) < 2):
            print "No file entered... exiting"
            return

        print "testing md5 sum on file : ", sys.argv[1]
        fname = sys.argv[1]
        print "md5sum => ", gen_hashsum(fname, 'md5')


if (__name__ == "__main__"):
    main()
