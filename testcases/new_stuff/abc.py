import hashlib 

def md5sum(fname): 
  """Computes md5 sum of input filename using hashlib library""" 
  """Example: md5sum( filename ) """

  try:
    fin = open (fname, 'rb')
  except:
    print 'Something wrong with file' , fname 
    exit() 
  
  hashsum = hashlib.md5()
  for contents in fin:
    hashsum.update (contents) 

  fin.close() 
  return hashsum.hexdigest()  




############### test env ############### 

import sys 
if (__name__ == "__main__"):
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

    print "testing md5 sum -- " , "on file : ", sys.argv[1]
    fname = sys.argv[1]
    # batch mode
    print "md5sum => ", md5sum(fname)
  

