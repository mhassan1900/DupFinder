import os
from os.path import join, getsize


def file_struct( cdir ):
  """file_struct creates a file data structure (hash table): 

  example: 
    {
      file_size1 : [file1]
      file_size2 : [file2, file3] 
      ...
      file_sizeM : [fileN]
    }

  where file2 and file3 have the same file_size2""" 

  file_dict = dict()    # will store size => [name, name, name]
  zero_bytes = list ()

  for root, dirs, files in os.walk( cdir ):
    for f in files: 
      filename = join(root, f)
      try:
        filesize = getsize(filename)
      except: # expect OSError
        print "WARNING. Problem getting file size info; file ", filename, " will not be included" 
        next 

      # print "name => ", filename  # for debug
      if (filesize == 0):
        zero_bytes.append (filename)    # modify for class
      elif (filesize in file_dict): 
        ( file_dict [filesize] ).append (filename)  
      else:
        file_dict [filesize] = [filename] 

  return file_dict


############### test env ############### 
import sys

if (__name__ == "__main__"):

  if (len(sys.argv) < 2):     # no of args 
    print "No directory entered... exiting"
    exit()

  mypath = sys.argv[1]

  print "-" * 60
  print "Testing file struct in directory: ", mypath
  print "-" * 60

  file_dict = file_struct( mypath )

  maxlen = 15
  for key in file_dict:
    spc = ' '*(maxlen - len(str(key)))
    if ( len(file_dict[key]) == 1 ):
      print key , spc , file_dict[key] 
    else:
      print key
      for f in file_dict[key]: 
        print ' ' * (maxlen + 3) , f



