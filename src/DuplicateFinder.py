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

import re 
import os
import os.path 
from hashsum import md5sum



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


    def dump (self, entry=1):
        """Dumps out data structure w/1 entry per line by default
        or a prettier version: .dump (n) where n > 1"""

        maxlen = 15

        print "-- File structure --"
        for k,v in self._file_dict.iteritems():
            spc = ' '*(maxlen - len(str(k)))

            if (entry == 1):
                print k , spc , v       # 1 entry per line
                continue 

            if ( len(v) == 1 ):     # only single file in list
                print k , spc , v 
            else:
                print k
                for f in v: 
                    print ' ' * (maxlen + 3) , f

        if ( len(self._zero_bytes) != 0 ): 
            print
            self.dump_zero_bytes()



    def dump_zero_bytes (self, entry=1):
        """Explicitly dumps files with 0 bytes"""

        print "-- Zero byte files --"
        if (entry == 1):
            print self._zero_bytes
        else:
            for f in self._zero_bytes: 
                print ' ' * (maxlen + 3) , f

        print



    # TODO. There is a big BUG in dump_duplicates(0) call!!
    def dump_duplicates (self, entry=1):
        """Displays duplicate files along with size in bytes"""

        print "-- Duplicate files --"
        maxlen =  15 
        excess_total = 0  

        for k,v in self._dup_fdict.iteritems():
            if (maxlen < len(str(k))):
                maxlen = len(str(k)) + 5
            spc = ' '*(maxlen - len(str(k)))

        excess_bytes = (len(v) - 2) * v[0] 
        excess_total +=  excess_bytes 

        if (entry == 1):
            print k , spc , v, " excess bytes: " , excess_bytes # 1 entry per line
        else:
            print k , spc,  v[0], " bytes each"
            print ' ' * (maxlen + 3) , excess_bytes, " bytes excess"
            for f in v[1:]: 
                print ' ' * (maxlen + 3) , f


        excess_total, qual = get_qual(excess_total) 
        print "-" * 40      
        print "Total excess space used: ", excess_total  , qual, "bytes"

        print


    # TODO. There might be a big BUG in dump_duplicates_log(0) call!!
    def dump_duplicates_log (self, entry=1):
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

    def _find_dup (self):

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




############### test env ############### 

if (__name__ == "__main__"):
    import sys
  
    if (len(sys.argv) < 2):     # no of args 
        print "No directory entered...switching to interactive mode"
        print "Enter directory for checking: "
        mypath = raw_input () 
    else:
        mypath = sys.argv[1]

    print "-" * 60
    print "Testing file struct generation" 
    print "-" * 60

    # 1. Create data structure
    dup_files = DuplicateFinder( mypath ) 
    dup_files.update( "/Users/mahmud/program/vstuff/timeout" ) 
    dup_files.dump(2) 
    # 2. Find duplictes 
    dup_files._find_dup()
    dup_files.dump_duplicates() 


