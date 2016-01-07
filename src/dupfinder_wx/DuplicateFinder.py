#!/usr/bin/env python
##########################################################################
# File:     DuplicateFinder.py
# Version:  0.10
# Author:   Mahmud Hassan
# Date:     July 2011
# License:  Lesser GPL ... 
# Summary:  Utility class to detect duplicate files 
#           This version is written in python (2.6+), so help or 
#           docstrings can be used to get more detailed documentation. 
##########################################################################

import sys
import re 
import os
import os.path 
from hashsum import md5sum, gen_hashsum, gen_partial_hashsums
import hashsum 


#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Standard functions 
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
def get_qual(fsize):
    """Returns file size qualifier"""
    if (fsize > 2**30): 
        fsize = fsize/float(2**30)
        qual =  'Giga'
    elif (fsize > 2**20): 
        fsize = fsize/float(2**20)
        qual =  'Mega'
    elif (fsize > 2**10): 
        fsize = fsize/float(2**10)
        qual =  'Kilo'
    else: qual = ''
    fsize = round(fsize, 2)
    return fsize, qual


def format_size(fsize, cround=2):
    """Returns str formatted size of fsize in bytes. Post conversion
    rounding given by cround"""
    fsize, qual = get_qual(fsize) 
    qual = qual[0] if qual != '' else '' # just use initial
    rsize = int(round(fsize,0)) if cround==0 else round(fsize,cround)
    fsize_str = str(rsize) + ' ' + qual + 'B' 
    return fsize_str 


def is_identical(fname1, fname2, hashtype='md5'):
    """Returns True if filenames fname1 and fname2 are identical, else False.
    If there was a problem with opening files, then returns None.
    Uses size and optionally hash compare to check"""

    errs = 0

    try:
        fsize1 = os.path.getsize(fname1)
    except: # expect OSError
        print "ERROR. Problem getting file size for file {}".format(fname1) 
        errs += 1

    try:
        fsize2 = os.path.getsize(fname2)
    except: # expect OSError
        print "ERROR. Problem getting file size for file {}".format(fname2) 
        errs += 1

    if errs > 0: 
        return None
    elif fsize1 != fsize2: 
        return False

    h1 = gen_hashsum(fname1, hashtype) 
    h2 = gen_hashsum(fname1, hashtype) 
    return True if (h1!=None and h2!=None and h1==h2) else False 




def search_and_insert(fgroups, fsize, hsum, fname): 
    """Search for [fsize, hsum, fname1, fname2, ...] within fgroups. If found,
    append fname to fname1, fname2, ... else create new list within fgroups.
    This is really a helper function for "group_indentical()" but could conceivably
    be used standalone.
    NOTE. fgroups is modified on entry being it is a list""" 

    if len(fgroups)==0:
        fgroups.append([fsize, hsum, fname])
    else: 
        for i, g in enumerate(fgroups):
            if fsize==g[0] and hsum==g[1]:
               fgroups[i].append(fname)
               return 
        fgroups.append([fsize, hsum, fname])
    return 



def group_identical(fsize, hashtype, *fnames): 
    """Groups a bunch of files into identical sets based on a hashsum type. 
    NOTE. Currently, expectation is that files are of same size"""

    chunksize = 2048 # min(hashsum._DEFAULT_CHUNK_, fsize)
    final = False if (fsize > 3*hashsum._DEFAULT_CHUNK_) else True
    # put into intial or final groups depending on size

    fgroups = []    # [(fsize, hsum, flist[]), (...), ... (...)]

    for fname in fnames: 
        if final: 
            hsum = gen_hashsum(fname, hashtype) 
        else:
            head, middle, tail = gen_partial_hashsums(fname, hashtype, chunksize)
            hsum = head + middle + tail     # string concat
        search_and_insert(fgroups, fsize, hsum, fname)

    if final:
        return fgroups

    newgroups = []    # [(fsize, hsum, flist[]), (...), ... (...)]

    for i, g in enumerate(fgroups):
        glist = g[2:]   
        hsums = [gen_hashsum(fname, hashtype) for fname in glist]
        for h, f in zip(hsums, glist):
            search_and_insert(newgroups, g[0], h, f)

    return newgroups 



#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# DuplicateFinder class definition
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
class DuplicateFinder:
    """File utility class to help find duplicate files."""

    """Initial implementation will only find identical files, but in the 
    future will add capability for some duplicate content as well, such as 
    images and music. This class provides the backend for a GUI as well.

    The primary data structure gathers file/data info with the following form: 

    {
      file_size1 : [file1]
      file_size2 : [file2, file3] 
      ...
      file_sizeM : [fileN]
    }

    where file2 and file3 have the same file_size2

    Several other lists are available, such as list of all root directories
    used to create the data struct and zero byte files 

    """ 

    # class variables

    # object variables 
    #   _root_dirlist   # maintain list of root directories provided
    #   _file_dict      # will store: {size : [name], size : [name, name, .. name], size : [name]}
    #   _zero_bytes     # list of zero byte files 
    #   _dup_fdict      # will store: {hashsum: [size, name], hashsum : [size, name, name, .. name], hashsum : [size, name]}


    def __init__ (self, dname=None):
        """Creates new class structure for files in directory""" 
      
        self._file_dict = dict()    
        self._zero_bytes = list()
        self._dup_fdict = dict()    
        self._found_dup = 0
        self._ignorelist = []   # explicit list of fully qualified directory name to ignore
        self._ignorematching = set( ['.svn', '.git'] ) # list of matching dirs to ignore by default

        if (dname == None):
            self._root_dirlist = []
        else:
            self._root_dirlist = ['dname'] 
            self.update (dname)


    def add2ignore (self, dname):
        """Add to list of directories with full path name to ignore"""
        if dname.strip() == '':
            return
        dname_full = os.path.abspath(dname.strip()) 
        if dname_full not in self._ignorelist: 
            self._ignorelist.append(dname_full)

       
    def update (self, dname):
        """Creates new class structure for files in directory using 
        obj.update(<directory_name>)""" 

        if (dname not in self._root_dirlist):  # TODO. weak attempt at not bloating database
                                               # ideally will inspect using regular exp. 
            self._root_dirlist.append (dname)
            self._create_fdict (dname)
            self._found_dup = 0                  # reset state to 0


    def dump_files (self):
        """Dumps out file data structure w/1 entry per line. Expects dictionary of {   
            key1: [file1, file2, ...], 
            key2: [file1, file2, ...], 
            keyN: [file1, file2, ...]
        }""" 

        print "-- File structure --"
        for k,vlist in self._file_dict.items():
            print '{:>20d} \t{}'.format(k, vlist[0])
            for v in vlist[1:]: 
                print '{:20s} \t{}'.format(' ', v)
            print '{:20s} \t{}'.format(' ', '-' * 80 )

        if len(self._zero_bytes) != 0: 
            print
            self.dump_zero_bytes()


    def dump_zero_bytes (self):
        """Explicitly dumps files with 0 bytes"""

        print "-- Zero byte files --"
        print '{:20s} \t{}'.format(' ', '-' * 80 )
        for v in self._zero_bytes:
            print '{:20s} \t{}'.format(' ', v) 
        print '{:20s} \t{}'.format(' ', '-' * 80 )


    def dump_duplicates (self):
        """Displays duplicate files along with size in bytes"""

        print "-- Duplicate files --"
        excess_total = 0  

        if len(self._dup_fdict) == 0: 
            print "No duplicates found" 
            return

        for k,vlist in self._dup_fdict.items():
            excess_bytes = (len(vlist) - 2) * vlist[0]     
            excess_total +=  excess_bytes 
            print '{:>20d} \t{}'.format( vlist[0], k )
            for v in vlist[1:]:
                print '{:>20s} \t{}'.format( ' ', v )
            print '{:>20d} \t{}'.format( excess_bytes, "bytes (excess)" ) 
            print '{:20s} \t{}'.format(' ', '-' * 80 )

        excess_total, qual = get_qual(excess_total) 
        print "-" * 40      
        print "Total excess space used: {} {}Bytes".format( excess_total , qual)
        print


    def dump_duplicates_log (self):
        """Displays duplicate files along with size in bytes, but returns
        the info into a 'log' list as opposed to the STDOUT"""

        logs = []
        logs.append("Duplicate files --")
        excess_total = 0  

        if len(self._dup_fdict) == 0: 
            logs.append( "No duplicates found" )
            logs.append("Total excess space used: 0 bytes")
            logs.append('') 
            return

        for k,vlist in self._dup_fdict.items():
            excess_bytes = (len(vlist) - 2) * vlist[0] 
            excess_total +=  excess_bytes 
            logs.append( '{:>20d} \t{} bytes each'.format( k, vlist[0] ) )
            logs.append( '{:>20d} \t{}'.format( excess_bytes, "bytes excess" ) ) 
            for v in vlist[1:]:
                logs.append( '{:>20s} \t{}'.format( ' ', v ) ) 

        excess_total, qual = get_qual(excess_total) 
        logs.append("-" * 40)     
        logs.append("Total excess space used: {} {}Bytes".format( excess_total , qual))
        logs.append('') 

        return logs


    def dump_duplicates_log_orig (self, entry=1):
        """Displays duplicate files along with size in bytes, but returns
        the info into a 'log' list as opposed to the STDOUT"""

        logs = []
        logs.append("Duplicate files --")
        maxlen =  15 
        excess_total = 0  

        for k,v in self._dup_fdict.iteritems():
            if (maxlen < len(str(k))):
                maxlen = len(str(k)) + 5
            spc = ' '*(maxlen - len(str(k)))

            excess_bytes = (len(v) - 2) * v[0] 
            excess_total +=  excess_bytes 

            if (entry == 1):
                logs.append( k + spc + v + " excess bytes: " + str(excess_bytes) ) 
            else:
                logs.append( k + spc +  str(v[0]) + " bytes each")
                logs.append( ' ' * (maxlen + 3) + str(excess_bytes) + " bytes excess")
                for f in v[1:]: 
                    logs.append( ' ' * (maxlen + 3) + f)

        logs.append("-" * 40)      # now compute total excess space

        excess_total, qual = get_qual(excess_total) 
        logs.append("Total excess space used: "+ str(excess_total)  + qual+ "bytes")
        logs.append('') 

        return logs


    def dump_duplicates_list (self):
        """Displays duplicate files along with size in bytes, in list format 
        primarily for gui use"""

        logs, sizes = [], []
        maxlen =  15 
        excess_total = 0  

        for k,v in self._dup_fdict.iteritems():
            excess_bytes = (len(v) - 2) * v[0] 
            excess_total +=  excess_bytes 

            bytes_str = format_size(v[0])
            excess_bytes_str = format_size(excess_bytes)

            logs.append( "## " + '-'*10 + ' ' + bytes_str + " each, " 
                          + excess_bytes_str + " excess" + ' ' + '-'*10  )
            sizes.append( 0 ) 

            for f in v[1:]: 
                logs.append( ' ' * 8 + f)
                sizes.append(v[0])

        bytes_total_str = format_size(excess_total)
        logs.append("## " + '-'*60) 
        logs.append("## Total excess space used: " + bytes_total_str) 
        logs.append("## " + '-'*60) 
        sizes.append( 0 ) 
        sizes.append( 0 ) 
        sizes.append( 0 ) 

        # for l in logs: print l # debug
        return logs, sizes


    def get_duplicates (self):
        """Returns dictionary of duplicates in following form:
           { 'md5sum' => [sz, file1, file2, ... fileN], ... } 
        """
        if (self._found_dup == 0):                  
            self._find_dup() 

        return self._dup_fdict



    #********************************************************
    # Private methods
    #********************************************************
    def _find_dup2 (self):
      """Main method that does searching"""

      for sz,vlist in self._file_dict.items():
          if (len(vlist) == 1): continue
          for fgroup in group_identical(sz, 'md5', *vlist):  # [sz, hsum, fname1, fname2]...
             hsum = fgroup[1] 
             if hsum in self._dup_fdict: 
                (self._dup_fdict[hsum]).extend(fgroup[2:]) 
             else:
                self._dup_fdict[hsum] = [sz]      # first entry of list is size 
                (self._dup_fdict[hsum]).extend(fgroup[2:]) 

      # now prune out the entries that have only 1 file 
      for h in  self._dup_fdict.keys(): 
        if ( len(self._dup_fdict[h]) < 3 ): 
                del self._dup_fdict [h]
      self._found_dup = 1                  
      return


    def _find_dup (self):
      """Main method that does searching"""

      for sz,v in self._file_dict.iteritems():
            if (len(v) == 1): continue

            for f in v: 
                hsum = md5sum(f)
                if (hsum in self._dup_fdict): 
                    (self._dup_fdict [hsum]).append(f) 
                else:
                    self._dup_fdict [hsum] = [sz]      # first entry of list is size 
                    (self._dup_fdict [hsum]).append(f) 

            # now prune out the entries that have only 1 file 
            for h in  self._dup_fdict.keys(): 
                if ( len(self._dup_fdict[h]) < 3 ): 
                    del self._dup_fdict [h]

      self._found_dup = 1                  



    def _create_fdict (self, cdir):
        """Returns dictionary of data structure"""

        ## print 'ignorelist', self._ignorelist # DEBUG

        cdir = os.path.abspath(cdir) ## print 'looking at ', absroot # DEBUG

        for root, dirs, files in os.walk( cdir ):

            root_tokens = set( re.split(r'[\/\\]', os.path.dirname(root) ) )
            if len(set(root_tokens).intersection(self._ignorematching)) > 0:
                ## print '--> matched', set(root_tokens).intersection(self._ignorematching)
                continue

            absroot = os.path.abspath(root) ## print 'looking at ', absroot # DEBUG
            ignore_files = False
            for iroot in self._ignorelist:
                if absroot.startswith(iroot):
                     ## print 'skipping ', root ## DEBUG
                     ignore_files = True
                     break
            if ignore_files: continue

            for f in files: 
                filename = os.path.join(root, f)
                try:
                    filesize = os.path.getsize(filename)
                except: # expect OSError
                    print "WARNING. Problem getting file size; file ", \
                        filename, " will not be included" 
                    continue 

                # print "name => ", filename  # for debug
                if (filesize == 0):
                    self._zero_bytes.append (filename)    
                elif (filesize in self._file_dict): 
                    (self._file_dict[filesize]).append (filename)  
                else:
                    self._file_dict [filesize] = [filename] 




#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Quick test environment 
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

_search_type_ = 1

def search_duplicates(*dirpaths):

    print "-" * 60
    print "Running duplicate file finder across followind directories" 
    dirpaths = [os.path.abspath(cdir) for cdir in dirpaths] 
    for d in dirpaths: print '  ', d
    print "-" * 60

    dupobj = DuplicateFinder( dirpaths[0] ) 
    for dpath in dirpaths[1:]:
        dupobj.update( dpath ) 
    dupobj.dump_files() 

    if _search_type_ == 2:
        dupobj._find_dup2()
    else:
        dupobj._find_dup()
    dupobj.dump_duplicates() 


if (__name__ == "__main__"):
    sys.path.insert  (0, '.')

    if (len(sys.argv) < 2):     # no of args 
        print "No directory entered...switching to interactive mode"
        print "Enter directory for checking: "
        mypath = raw_input () 
    else:
        search_duplicates(*sys.argv[1:])
        # mypath = sys.argv[1]


    ## 1. Create data structure
    #dup_files = DuplicateFinder( mypath ) 
    #dup_files.update( "/Users/mahmud/program/vstuff/timeout" ) 
    #dup_files.dump(2) 
    ## 2. Find duplictes 
    #dup_files._find_dup()
    #dup_files.dump_duplicates() 


