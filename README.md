Use Dupfinder to find duplicate files (via command line or desktop GUI) from a given set of directories.
It uses a combination of file sizes and hashsum signatures today to detect and report exact duplicates.

Features
--------
    1. Find and display duplicates from a list of directories.
    2. In compare mode, finds duplicates from exactly two directories, and displays in two columns files that are duplicate.
    3. Display disk space taken up by each duplicate, as well as aggregate space.
    4. Exclude certain directories from search or reporting [.git, .svn excluded by default].
    5. Exclude certain filename patterns from being considered.
    6. In GUI mode, interactively select files for deletion, with confirmation.
    7. In GUI mode, interactively select and open files for viewing [OS dependent].


OS Support
----------
    1. MacOS
    2. Linux (last feature may not be supported)
    3. Windows (last feature may not be supported)


Screenshots
-----------
- GUI Mode Example
![GUI Mode Example](https://raw.githubusercontent.com/mhassan1900/DupFinder/master/docs/gui-example.png "GUI Example")

- Command Line Usage
![Command Line Usage](https://raw.githubusercontent.com/mhassan1900/DupFinder/master/docs/cmd-usage.png "CMD Line Usage")


Execution
---------
- Preferred approach. Install (into user directory) or root application location, and type:
```
dupfinder                             # Shows help and options
dupfinder -d testcases/sample_files   # Run on provided sample
dupfinder -g                          # Brings up GUI
```
- Alternate method. There are separate scripts included for GUI & command line execution:   
```
  ./scripts/dupfinder
  ./scripts/dupfinder -d testcases/sample_files
  ./scripts/dupfinder_gui
```


Installation
------------
`make install` # this will install the scripts under user's site-packages directory by default.

Type `make` by itself for more options


Dependencies
------------
- python2.7
- wxpython 3.0 or higher
