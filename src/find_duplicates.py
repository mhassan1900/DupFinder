#!/Users/mahmud/bin/python
"""
##########################################################################
# File:     find_duplicate_files.py 
# Version:  0.10
# Author:   Mahmud Hassan
# Date:     July 2011
# License:  Lesser GPL ... 
# Summary:  Script to generate info on duplicate files
#           This version is written in python (2.6+), so help or 
#           docstrings can be used to get more detailed documentation. 
##########################################################################

Usage: 
        find_duplicate_files.py <dir1> ... <dirN> [option] #  batch mode 
        find_duplicate_files.py                            #  interactive mode  

        [option] must be one of -help or -column

"""


import DuplicateFinder 
import sys

DEBUG = False


def Usage():
    """Prints help and usage message"""
    print __doc__
    exit()



def main():
   """Executes duplicate file finder functions by building data-structure
   and calling methods"""

   # ------------------------
   # argument parsing section
   # ------------------------
   interactive = (len(sys.argv) < 2)   # non-interactive 
   col_mode = True                     # by default map to 2 roots/column mode 

   if interactive: 
      print "No directory entered...switching to interactive mode"
      print "Enter directories separated by space for checking: "
      try: 
          mypath_str = raw_input () 
      except KeyboardInterrupt:     # eg, hit CTRL-C
          print
          exit() 

      mypath_list = mypath_str.split()

   else:    # batch mode
      sys.argv.pop(0)
      mypath_list = sys.argv

   # check for switches 
   if ('-help' in mypath_list) or ('-h' in mypath_list):   Usage() 

   if '-column' in mypath_list: mypath_list.remove('-column') 
   elif '-col'  in mypath_list: mypath_list.remove('-col') 
   elif '-c'    in mypath_list: mypath_list.remove('-c') 
   else:
       col_mode = False
       

   if col_mode and (len(mypath_list) != 2):
       print "ERROR. Column mode must have only 2 roots!" 
       Usage()



   # initialize & then update
   # ------------------------
   print "** 1. Creating file/directory structure **" 

   dup_files = DuplicateFinder.DuplicateFinder() 

   for mypath in mypath_list:
       dup_files.update(mypath) 
       print "      Building structure for: ", mypath


   if (DEBUG): dup_files.dump()
   print "-- Directory structure creation complete --\n"


   # report duplicates
   # -----------------
   print "** 2. Finding duplicates **"

   dup_table = dup_files.get_duplicates()


   if not col_mode:
       
       print '-' * 70
       print "  Raw table { 'md5sum1' : [sz, file1, file2, file3, ...], ... }"  
       print '-' * 70

       # NOTE. There is a big BUG in dump_duplicates(0) call!!
       # dup_files.dump_duplicates(0)  
       logs, sizes = dup_files.dump_duplicates_list()
       for l in logs: print l
       return


   # else start the more exhaustive search
   # data-structure conversion routine
   # ----------------------------------------
   root1 = mypath_list.pop() 
   root2 = mypath_list.pop() 

   # each of these will store a list of lists 
   root1_list = []   
   root2_list = []

   import re

   for flist in dup_table.values():
        # print "flist => ", flist - all files in list have same content 
        sz = flist.pop(0) 
        flist1 =  [] 
        flist2 =  [] 
        for fname in flist:
            if re.search(r'/.svn', fname):       # skip ".svn" files
                continue
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
   main()   
   

