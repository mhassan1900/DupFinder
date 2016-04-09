#!/usr/bin/env ipython


# hierarchy
# find_duplicates_wxtop
# - _wxmainpanel
# - _wxstdpanel 
# - _wxcmppanel 


import os
import os.path 
import DuplicateFinder as Dup
import wx

_DEFWIDTH_ = 500
_BUTWIDTH_ = 130 

import multiprocessing as mp


### -- BEGIN OF PROGRESS DIALOG --
from wx.lib.pubsub import pub
#from threading import Thread

#   class TestThread(Thread):
#       """Test Worker Thread Class."""
#    
#       #----------------------------------------------------------------------
#       def __init__(self):
#           """Init Worker Thread Class."""
#           Thread.__init__(self)
#           self.start()    # start the thread
#    
#       #----------------------------------------------------------------------
#       def run(self):
#           """Run Worker Thread."""
#           # This is the code executing in the new thread.
#           for i in range(20):
#               wx.Sleep(1)
#               wx.CallAfter(pub.sendMessage, "update", msg="")



# class MyProgressDialog(wx.Dialog):
class MyProgressDialog(wx.ProgressDialog):
    """Dialog box that can receive updates from a thread"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        # wx.Dialog.__init__(self, None, title="Progress")
        wx.ProgressDialog.__init__(self, title='Finding Duplicates', message='Working', maximum=100, parent=None,
               style=wx.PD_AUTO_HIDE | wx.PD_ELAPSED_TIME) #  | wx.PD_APP_MODAL)

        self.count = 0
        # self.progress = wx.Gauge(self, range=20)
        #sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(self.progress, 0, wx.EXPAND)
        #self.SetSizer(sizer)
 
        # create a pubsub receiver
        pub.subscribe(self.updateProgress, "update")
 
    #----------------------------------------------------------------------
    def updateProgress(self, msg):
        """"""
        self.count += 1
 
        #if self.count >= 20:
        #    self.Destroy()
        # 
        # self.progress.SetValue(self.count)
        self.Update(self.count)


### -- END OF PROGRESS DIALOG --


#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# StdPanel class definition
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


class MainPanel(wx.Panel):

    def __init__(self, parent, stdpanel=None, cmppanel=None):
        '''Custom panel that has most of the functionality of the DupFinder GUI. 
        It expects to pass data to a stdpanel & cmppanel for display & processing.
        These two are needed during initialization OR set later on via set_stdview()
        and set_cmpview()'''

        wx.Panel.__init__(self, parent=parent)

        # variables need for non-GUI execution
        self.dirlist = []               # list of directories to search
        self.ignorelist = []            # list of directories to ignore
        self.srch_results_list = []     # list of names in search results (includes comments)
        self.srch_sizes_list = []       # list of sizes from search results
        self.filesel_list = []          # list of (checked) selections from search results

        self.stdpanel = stdpanel
        self.cmplanel = cmppanel

        self.initUI()                   # create all the widgets
        self.configureUI()              # configures widgets additionally 
        self.displayUI()                # display them appropriately
        self.bindUI()                   # bind the functions 


    # -------------------------- GUI Components -------------------------- 
    # Initialization, Configuration, Placement 
    # -------------------------------------------------------------------- 
    def initUI(self):
        """Initializes all the widgets in the UI. It does not include
        geometry configuration, or other detailed config beyond basic 
        initialization and variable or commmand binding"""

        self.rb_finddup = wx.RadioButton(self, label='Find Duplicates') # , value=FIND_MODE)  
        self.rb_compare = wx.RadioButton(self, label='Compare Folders') 

        # -- prefix 1 is for adding to search list -- 
        self.t_add1 = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(_DEFWIDTH_-160,-1)) 
        self.b_del1 = wx.Button(self, label='-', size=(30,-1))
        self.st_dirs1 = wx.StaticText(self, label='Folders to search', size=(_DEFWIDTH_-_BUTWIDTH_,-1)) 
        self.lbx_dirs1 = wx.ListBox(self, choices=[], style=wx.HSCROLL|wx.LB_NEEDED_SB|wx.LB_EXTENDED)

        self.b_sel1 = wx.Button(self, label='Select Folder(s)', size=(_BUTWIDTH_,-1))
        self.b_search = wx.Button(self, label='Search')
        self.b_clearfolders = wx.Button(self, label='Clear Folders')
        self.b_clearconsole = wx.Button(self, label='Clear Console')    #TODO.
        self.b_quit = wx.Button(self, label='Quit')

        # -- prefix 2 is for adding to exclude list -- 
        self.t_add2 = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(_DEFWIDTH_-160,-1)) 
        self.b_del2 = wx.Button(self, label='-', size=(30,-1))
        self.st_dirs2 = wx.StaticText(self, label='Folders to exclude', size=(_DEFWIDTH_-_BUTWIDTH_,-1)) 
        self.lbx_dirs2 = wx.ListBox(self, choices=[], style=wx.HSCROLL|wx.LB_NEEDED_SB|wx.LB_EXTENDED)

        self.st_extraopt = wx.StaticText(self, label='(Extra Options)')
        self.b_sel2 = wx.Button(self, label='Select Exclusion(s)', size=(_BUTWIDTH_,-1))
        self.b_skipmatch = wx.Button(self, label='Skip Matches')

        self.st_console = wx.StaticText(self, label='Console') 
        self.t_console = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.VSCROLL|wx.TE_READONLY, 
                size=(_DEFWIDTH_,100))
        self.sb_status = wx.StatusBar(self)



    # -------------------------------------------------------------------------------- #
    def configureUI(self):
        """Performs additional configuration of GUI beyond just simple initialization, 
        especially when related to geometries""" 
        
        self.t_add1.SetValue('Type in folder name & hit Enter to add to search. Press (-) to remove selections.') 
        self.t_add2.SetValue('Type in folder name & hit Enter to add to exclusions. Press (-) to remove selections.') 
        self.t_add1.SelectAll()
        self.t_add2.SelectAll()
        self.rb_finddup.SetValue(True)  # default mode 
        self.sb_status.SetFieldsCount(2)
        #self.sb_status.SetStatusText( \
        #    "Steps: [1] Select folder(s) [2] Hit Search [3] Left mouse to select files, Right click to take action") 
        self.sb_status.SetStatusWidths([-3, -1]) # doen't seem to work
        self.sb_status.SetFields( ['Steps: [1] Select folder(s) [2] Search [3] Choose a tab', '->']) 
        ## self.g_progress = wx.Gauge(self.sb_status, style=wx.GA_HORIZONTAL|wx.GA_SMOOTH) 
       


    # -------------------------------------------------------------------------------- #
    def displayUI(self):
        """Actually displays the different widgets of the UI. Has most of the grid 
        packing rules in here""" 

        mainsizer = wx.BoxSizer(wx.VERTICAL)     # break up into rows
        hsizer1   = wx.BoxSizer(wx.HORIZONTAL)     # for row 1

        # repeat this sequence for **Extra Options**
        hsizer2   = wx.BoxSizer(wx.HORIZONTAL)     # for row 2
        vsizer2l  = wx.BoxSizer(wx.VERTICAL)     # for row 2.L
        vsizer2r  = wx.BoxSizer(wx.VERTICAL)     # for row 2.R
        hsizer2r1 = wx.BoxSizer(wx.HORIZONTAL) # for row 2.R.1
        hsizer2r2 = wx.BoxSizer(wx.HORIZONTAL) # for row 2.R.2

        # for **Extra Options**
        hsizer3   = wx.BoxSizer(wx.HORIZONTAL)     # for row 3
        vsizer3l  = wx.BoxSizer(wx.VERTICAL)     # for row 3.L
        vsizer3r  = wx.BoxSizer(wx.VERTICAL)     # for row 3.R
        hsizer3r1 = wx.BoxSizer(wx.HORIZONTAL) # for row 3.R.1
        hsizer3r2 = wx.BoxSizer(wx.HORIZONTAL) # for row 3.R.2

        hsizer1.Add(self.rb_finddup, 1, flag=wx.EXPAND) 
        hsizer1.Add(self.rb_compare, 1, flag=wx.EXPAND)

        # -- row 2 stuff --
        # row2, right - textctrl & buttons 
        hsizer2r1.Add(self.st_dirs1, flag=wx.EXPAND)
        hsizer2r2.Add(self.t_add1, 1, flag=wx.EXPAND)
        hsizer2r2.Add(self.b_del1)

        vsizer2r.Add(hsizer2r1, flag=wx.EXPAND)
        vsizer2r.Add(hsizer2r2, flag=wx.EXPAND)
        vsizer2r.Add(self.lbx_dirs1, 1, flag=wx.EXPAND)

        # row2, left - buttons 
        dummy1 = wx.StaticText(self, label=' ')
        buttons = [dummy1, self.b_sel1, self.b_search, self.b_clearfolders, self.b_clearconsole, self.b_quit] 
        for b in buttons: vsizer2l.Add(b, 0, flag=wx.EXPAND)  

        # row2 main 
        hsizer2.Add(vsizer2l, 0, flag=wx.EXPAND)
        hsizer2.Add(vsizer2r, 1, flag=wx.EXPAND)


        # -- row 3 stuff --
        # row3, right - textctrl & buttons 
        hsizer3r1.Add(self.st_dirs2, 1, flag=wx.EXPAND)
        hsizer3r2.Add(self.t_add2, 1, flag=wx.EXPAND)
        hsizer3r2.Add(self.b_del2)

        vsizer3r.Add(hsizer3r1, flag=wx.EXPAND)
        vsizer3r.Add(hsizer3r2, flag=wx.EXPAND)
        vsizer3r.Add(self.lbx_dirs2, flag=wx.EXPAND)

        # row3, left - buttons 
        leftstuff = [self.st_extraopt, self.b_sel2, self.b_skipmatch] 
        for b in leftstuff: vsizer3l.Add(b, 0, flag=wx.EXPAND)  

        # row3 main 
        hsizer3.Add(vsizer3l, 0, flag=wx.EXPAND)
        hsizer3.Add(vsizer3r, 1, flag=wx.EXPAND)


        # -- now add all the rows/sizers -- 
        mainsizer.Add(hsizer1, 0, flag=wx.EXPAND) 
        mainsizer.AddSpacer(5)
        mainsizer.Add(hsizer2, 0, flag=wx.EXPAND) 
        mainsizer.AddSpacer(10)
        mainsizer.Add(hsizer3, 0, flag=wx.EXPAND) 
        mainsizer.AddSpacer(10)
        mainsizer.Add(self.st_console, 0)
        mainsizer.Add(self.t_console, 1, flag=wx.EXPAND)
        mainsizer.Add(self.sb_status, 0, flag=wx.EXPAND)
        self.SetSizer(mainsizer)

        self.Fit()
        


    # -------------------------------------------------------------------------------- #
    def bindUI(self):               
        """Binds any mouse functions to the widgets in this section"""

        self.t_add1.Bind(wx.EVT_TEXT_ENTER, self.onAdd1)
        self.b_del1.Bind(wx.EVT_BUTTON, self.onDel1)
        self.b_sel1.Bind(wx.EVT_BUTTON, self.onSeldir1)

        self.t_add2.Bind(wx.EVT_TEXT_ENTER, self.onAdd2)
        self.b_del2.Bind(wx.EVT_BUTTON, self.onDel2)
        self.b_sel2.Bind(wx.EVT_BUTTON, self.onSeldir2)

        self.b_search.Bind(wx.EVT_BUTTON, self.onSearch)  
        self.b_skipmatch.Bind(wx.EVT_BUTTON, self.onSkipMatch)  
        self.b_clearfolders.Bind(wx.EVT_BUTTON, self.onClearFolders)
        self.b_clearconsole.Bind(wx.EVT_BUTTON, self.onClearConsole) 

        # relegate this to top level (ie, frame)
        # ----------------------------------------
        #self.b_quit.Bind(wx.EVT_BUTTON, self.quitApp)  
        #self.Bind(wx.EVT_CLOSE, self.quitApp)  




    # -------------------------- Widget Actions  ------------------------- #
    # Related Methods but not directly connected to any event 
    # -------------------------------------------------------------------- #

    def set_stdview(self, panel): 
        '''Sets the std view via a panel''' 
        self.stdpanel = panel


    def set_cmpview(self, panel): 
        '''Sets the std view via a panel''' 
        self.cmppanel = panel


    def cprint (self, s='\n'): 
        """Abstracts out console printing whether TextCtrl or otherwise"""
        self.t_console.AppendText(s)



    # -------------------------- Widget Actions  -------------------------- #
    # Direct Bindings (callbacks) - respond to events 
    # --------------------------------------------------------------------- #


    # -------------------------------------------------------------------------------- #
    # ------------------------ Related to the buttons on left ------------------------ #
    # -------------------------------------------------------------------------------- #

    def onSearch(self, e=None):
        """Function that invokes the routine for duplicate file finding"""


        compare_mode = self.rb_compare.GetValue() 
        
        if compare_mode:
            self.cprint('** Compare View Mode **\n') 
        else:
            self.cprint('** Standard View Mode **\n') 


        self.cprint('** 1. Creating file/directory structure **\n')

        dup_obj = Dup.DuplicateFinder() 

        for p in self.ignorelist:       #TODO. Check if used
           ## self.cprint ("p => " + p + "\n") 
           ## if os.path.exists(p):    # should always exist...
           self.cprint('   Ignoring everthing under: {}\n'.format(p)) #  os.path.abspath(p) + "\n")
           dup_obj.add2ignore(os.path.abspath(p))
       

        self.cprint()
        self.cprint( 'INFO. matched dirs (relative) to exclude:' )
        self.cprint( repr(dup_obj._ignorematching) +'\n' )

        # go by what is in dirlist NOT what is displayed    # TODO
        for p in self.dirlist:
           dup_obj.update(p) 
           self.cprint('   Building structure for: {}'.format(p)) 

        self.cprint()
        self.cprint("-- Directory structure creation complete --\n")
        self.cprint("** 2. Finding duplicates **\n")

        # -- progress bar indicator --
        ## TestThread()
        ## p_dlg = MyProgressDialog()
        
        #p_dlg = wx.ProgressDialog(title='Finding Duplicates', message='Working', maximum=100, parent=None,
        #      style=wx.PD_AUTO_HIDE | wx.PD_ELAPSED_TIME) #  | wx.PD_APP_MODAL)

        ## -- Separate thread --
        #keepGoing = True 
        #count = 0
        #while keepGoing and count < 100:
        #   count = count + 1
        #   wx.Sleep(1)
        #   keepGoing = p_dlg.Update(count)
        # -- ------
        
        dup_table = dup_obj.get_duplicates()        # <-- this should be on one thread

        #p1 = mp.Process(target=dup_obj.get_duplicates)
        #p1.start()
        #self.cprint("-- Please wait until dupfinder completes --")
        #p1.join()
        #return

        ## p_dlg.Destroy() 

        #TODO. This stuff is redundant now...
        ## self.srch_results_list, self.srch_sizes_list =  dup_obj.dump_duplicates_list()


        self.cprint("-- Duplicate listing complete --\n")

        if compare_mode:
            if len(self.dirlist) != 2: 
                self.cprint('ERROR. You must have 2 folders to perform search in compare mode\n') 
                wx.MessageBox('You must have 2 folders to perform search in compare mode', 
                    style=wx.ICON_ERROR) 
                return
            self.cmppanel.dup_table = dup_table
            self.cmppanel.dirlist = self.dirlist
            self.cmppanel.ignorelist = self.ignorelist
            self.cmppanel.displayDuplicates()
            self.cprint('** Check "Compare View" tab for results **\n') 
        else:       
            self.stdpanel.dup_table = dup_table
            self.stdpanel.dirlist = self.dirlist
            self.stdpanel.ignorelist = self.ignorelist
            self.stdpanel.displayDuplicates()
            ## for t in self.srch_results_list: self.cprint(t+'\n')  # for DEBUG
            self.cprint('** Check "Standard View" tab for results **\n') 

        self.cprint()

        ##print 'DUP TABLE (DEBUG)' 
        ##for k,v in dup_table.items(): print k, '->', v


    # -------------------------------------------------------------------------------- #
    def onSkipMatch(self, e=None):
        """Enters the matched dirs/filenames to skip"""
        pass



    # -------------------------------------------------------------------------------- #
    def onClearFolders(self, e=None):
        """Clears all directory lists"""
        self.dirlist = []
        self.ignorelist = []
        self.t_add1.Clear()
        self.t_add2.Clear()
        self.lbx_dirs1.Set([])
        self.lbx_dirs2.Clear() 



    # -------------------------------------------------------------------------------- #
    def onClearConsole(self, e=None):
         """Clears the console in the window"""
         self.t_console.SetValue('')


    # -------------------------------------------------------------------------------- #
    def checkValidDir(self, dpath):
        """Checks if directory path is valid for entry. Returns False if it is not"""

        compare_mode = self.rb_compare.GetValue() 
        if compare_mode: 
            if len(self.dirlist) >= 2: 
                self.cprint ("ERROR. Cannot add more than 2 directories into search list in 'Compare Mode'\n") 
                return False
        
        if not os.path.exists(dpath):
            self.cprint("Warning. Dir path does not exist. %s will not be added\n" % (dpath))    
            return False
        elif dpath in self.dirlist:
            self.cprint ("Warning. Dir already added to search list. %s will not be added\n" % (dpath))
            return False

        return True
        

    # -------------------------------------------------------------------------------- #
    def onAdd1(self, e=None):
        """Adds directory entry into list of search dirs""" 

        dpath = self.t_add1.GetValue().strip('\n').strip()
        if dpath == '': 
            return
        elif self.checkValidDir(dpath):
            self.dirlist.append(dpath)  
            self.lbx_dirs1.AppendAndEnsureVisible(dpath)

       #compare_mode = self.rb_compare.GetValue() 
       #if compare_mode: 
       #    if len(self.dirlist) == 2: 
       #        self.cprint ("ERROR. Cannot add more than 2 directories into search list in 'Compare Mode'\n") 
       #        return
       #    

       #dpath = self.t_add1.GetValue().strip('\n').strip()


       #if dpath == '': 
       #    return
       #elif dpath in self.dirlist:
       #    self.cprint ("Warning. Dir already added to search list. %s will not be added\n" % (dpath))
       #elif os.path.exists(dpath):
       #    self.dirlist.append(dpath)  # superfluous?
       #    self.lbx_dirs1.AppendAndEnsureVisible(dpath)
       #else:
       #    self.cprint("Warning. Dir path does not exist. %s will not be added\n" % (dpath))    


    # -------------------------------------------------------------------------------- #
    def onAdd2(self, e=None):
        """Adds directory entry into list of exclude dirs""" 

        dpath = self.t_add2.GetValue().strip('\n').strip()

        if dpath == '': 
            return
        elif dpath in self.ignorelist:
            self.cprint ("Warning. Dir already added to exclude list. %s will not be added\n" % (dpath))
        elif os.path.exists(dpath):
            self.ignorelist.append(dpath)  # superfluous?
            self.lbx_dirs2.AppendAndEnsureVisible(dpath)
        else:
            self.cprint("Warning. Dir path does not exist. %s will not be added\n" % (dpath))    


 
    # -------------------------------------------------------------------------------- #
    def onDel1(self, e=None):
        """Removes directory entry from list of search dirs""" 

        if len(self.dirlist) < 1:
            return 

        idxlist = list(self.lbx_dirs1.GetSelections())
        idxremain = filter( lambda x: x not in idxlist, range(len(self.dirlist)) ) 
        tmplist = [self.dirlist[i] for i in idxremain]
        self.dirlist = tmplist
        self.lbx_dirs1.Set(tmplist)


 
    # -------------------------------------------------------------------------------- #
    def onDel2(self, e=None):
        """Removes directory entry from list of exclude dirs""" 

        if len(self.ignorelist) < 1:
            return 

        idxlist = list(self.lbx_dirs2.GetSelections())
        idxremain = filter( lambda x: x not in idxlist, range(len(self.ignorelist)) ) 
        tmplist = [self.ignorelist[i] for i in idxremain]
        self.ignorelist = tmplist
        self.lbx_dirs2.Set(tmplist)


 

    # -------------------------------------------------------------------------------- #
    def onSeldir1(self, e=None):
       """Selects dir from ask open folder dialog box""" 
       
       ddsel = wx.DirDialog(self, "Choose a directory", style=wx.DD_DEFAULT_STYLE|wx.DD_DIR_MUST_EXIST) 
       if ddsel.ShowModal() != wx.ID_OK: 
           ddsel.Destroy()
           return 

       dpath = ddsel.GetPath() 

       if not self.checkValidDir(dpath):
           return
#      if dpath in self.dirlist:
#          self.cprint("Warning. Dir already added to list. %s will not be added\n" % (dpath))
#          return

       self.dirlist.append(dpath)
       self.lbx_dirs1.AppendAndEnsureVisible(dpath)
       # also populate entry box with same
       self.t_add1.SetValue(dpath)
       self.t_add1.SetSelection(-1,-1) 



    # -------------------------------------------------------------------------------- #
    def onSeldir2(self, e=None):
       """Selects dir from ask open folder dialog box""" 
       
       ddsel = wx.DirDialog(self, "Choose a directory", style=wx.DD_DEFAULT_STYLE|wx.DD_DIR_MUST_EXIST) 
       if ddsel.ShowModal() != wx.ID_OK: 
           ddsel.Destroy()
           return 

       dpath = ddsel.GetPath() 
       if dpath in self.ignorelist:
           self.cprint("Warning. Dir already added to ignore list. %s will not be added\n" % (dpath))
           return
 
       self.ignorelist.append(dpath)
       self.lbx_dirs2.AppendAndEnsureVisible(dpath)
       # also populate entry box with same
       self.t_add2.SetValue(dpath)
       self.t_add2.SetSelection(-1,-1) 



    # -------------------------- Widget Actions  -------------------------- 
    # Right-click/Popup Menu options
    # -------------------------------------------------------------------- 


#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Other standard functions 
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>



