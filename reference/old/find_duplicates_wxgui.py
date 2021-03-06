#!/usr/bin/env ipython

import os
import os.path 
import DuplicateFinder as Dup
import wx

_DEFWIDTH_ = 600

#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# MyApp class definition
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


class MyFrame(wx.Frame):
    """Top level GUI application window"""

    def __init__(self, title=None):
        wx.Frame.__init__(self, parent=None, title=title)

        # variables need for non-GUI execution
        self.dirlist = []               # list of directories to search
        self.ignorelist = []            # list of directories to ignore
        self.srch_results_list = []     # list of names in search results (includes comments)
        self.srch_sizes_list = []       # list of sizes from search results
        self.filesel_list = []          # list of (checked) selections from search results

        # actuate the GUI 
        self.initUI()           # create all the widgets
        self.configureUI()      # configures widgets additionally 
        self.displayUI()        # display them appropriately
        self.bindUI()           # bind the functions 


    # -------------------------- GUI Components -------------------------- 
    # Initialization, Configuration, Placement 
    # -------------------------------------------------------------------- 
    def initUI(self):
        """Initializes all the widgets in the UI. It does not include
        geometry configuration, or other detailed config beyond basic 
        initialization and variable or commmand binding"""


        self.rb_finddup = wx.RadioButton(self, label='Find Duplicates') # , value=FIND_MODE)  
        self.rb_compare = wx.RadioButton(self, label='Compare Folders') 

        self.t_add1 = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(_DEFWIDTH_-100,-1)) 
        self.b_add1 = wx.Button(self, label='+')
        self.b_del1 = wx.Button(self, label='-')

        self.b_sel1 = wx.Button(self, label='Select Folder(s)')
        self.b_search = wx.Button(self, label='Search')
        self.b_clearfolders = wx.Button(self, label='Clear Folders')
        self.b_clearresults = wx.Button(self, label='Clear Results')
        self.b_quit = wx.Button(self, label='Quit')

        self.st_dirs1 = wx.StaticText(self, label='Folders to search', size=(_DEFWIDTH_-100,-1)) 
        self.lbx_dirs1 = wx.ListBox(self, choices=[], style=wx.HSCROLL|wx.LB_NEEDED_SB|wx.LB_EXTENDED)
        self.st_results = wx.StaticText(self, label='Search results') 
        self.clbx_results = wx.CheckListBox(self, style=wx.HSCROLL|wx.LB_NEEDED_SB|wx.LB_EXTENDED, 
            choices=[], size=(_DEFWIDTH_,300))
        self.st_console = wx.StaticText(self, label='Console') 
        self.t_console = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.VSCROLL|wx.TE_READONLY, 
                size=(_DEFWIDTH_,100))
        self.sb_status = wx.StatusBar(self)

        self.popupmenu = self.createPopupMenu()

        #TODO. for future 
        self.t_add2 = wx.TextCtrl(self) 
        self.b_add2 = wx.Button(self, label='+') 
        self.b_sel2 = wx.Button(self, label='Select Folder (Compare)')   
        self.st_dirs2 = wx.StaticText(self, label='Folders to compare') 


        futures = [self.b_add2, self.t_add2, self.b_sel2, self.st_dirs2] 
        for f in futures: f.Hide()


    def configureUI(self):
        """Performs additional configuration of GUI beyond just simple initialization, 
        especially when related to geometries""" 
        
        self.t_add1.SetValue('You may type in folder name directly to add (+)') 
        self.sb_status.SetStatusText( \
            "Steps: [1] Select folder(s) [2] Hit Search [3] Left mouse to select files, Right click to take action") 


    def displayUI(self):
        """Actually displays the different widgets of the UI. Has most of the grid 
        packing rules in here""" 

        mainsizer = wx.BoxSizer(wx.VERTICAL)     # break up into rows
        hsizer1   = wx.BoxSizer(wx.HORIZONTAL)     # for row 1
        hsizer2   = wx.BoxSizer(wx.HORIZONTAL)     # for row 2
        vsizer2l  = wx.BoxSizer(wx.VERTICAL)     # for row 2.L
        vsizer2r  = wx.BoxSizer(wx.VERTICAL)     # for row 2.R
        hsizer2r1 = wx.BoxSizer(wx.HORIZONTAL) # for row 2.R.1
        hsizer2r2 = wx.BoxSizer(wx.HORIZONTAL) # for row 2.R.2

        # row1 - radio buttons
        hsizer1.Add(self.rb_finddup)
        hsizer1.Add(self.rb_compare)

        # row2, right - textctrl & buttons 
        hsizer2r1.Add(self.t_add1, 1, flag=wx.EXPAND)
        hsizer2r1.Add(self.b_add1)
        hsizer2r2.Add(self.st_dirs1, 1, flag=wx.EXPAND)
        hsizer2r2.Add(self.b_del1)

        vsizer2r.Add(hsizer2r1, flag=wx.EXPAND)
        vsizer2r.Add(hsizer2r2, flag=wx.EXPAND)
        vsizer2r.Add(self.lbx_dirs1, flag=wx.EXPAND)

        # row2, left - buttons 
        buttons = [self.b_sel1, self.b_search, self.b_clearfolders, self.b_clearresults, self.b_quit] 
        for b in buttons: vsizer2l.Add(b, 1, flag=wx.EXPAND)  

        # vsizer2r.RecalcSizes()

        # row2
        hsizer2.Add(vsizer2l, 0, flag=wx.EXPAND)
        hsizer2.Add(vsizer2r, 1, flag=wx.EXPAND)


        # now add all the rows/sizers
        mainsizer.Add(hsizer1) 
        mainsizer.AddSpacer(5)
        mainsizer.Add(hsizer2, 0, flag=wx.EXPAND) 
        mainsizer.AddSpacer(5)
        mainsizer.Add(self.st_results, 0)
        mainsizer.Add(self.clbx_results, 1, flag=wx.EXPAND)
        mainsizer.Add(self.st_console, 0)
        mainsizer.Add(self.t_console, flag=wx.EXPAND)
        mainsizer.Add(self.sb_status, 0)
        self.SetSizer(mainsizer)

        self.Fit()
        self.Show()
        

    def set_find_mode(self):
        self.comp_modevar.set(FIND_MODE) 
        self.b_search.configure(text='Search', command=self.search)
    
        # <><>-- IGNORE ALL FOR NOW --<><>
        # forget/remove the other stuff
        ##  self.b_add2.grid_forget()
        ##  self.e_add2.grid_forget()
        ##  self.b_sel2.grid_forget() 
        ##  self.lbfm2.grid_forget()
        ##  self.label_dirs2.grid_forget()
        ##  self.lbfm_console2.grid_forget()
        ##  self.lbx_console2.grid_forget()



    def set_comp_mode(self):
        # self.comp_modevar.set(FIND_MODE) # self.comp_modevar.set(COMP_MODE) 
        # return
        pass



    def createPopupMenu(self):               
        item_names = ['Delete', 'Clear Selections', 'Open Enclosing Folder', 'Open File'] 
        item_funcs = [self.deleteFile, self.clearSelections, self.openFolder, self.openFile] 

        pmenu = wx.Menu()

        for (iname,ifunc) in zip(item_names,item_funcs):
            item = pmenu.Append(-1, iname)
            self.Bind(wx.EVT_MENU, ifunc, item)
    
        return pmenu



    def bindUI(self):               
        """Binds any mouse functions to the widgets in this section"""

        self.t_add1.Bind(wx.EVT_TEXT_ENTER, self.add1)
        self.b_add1.Bind(wx.EVT_BUTTON, self.add1)
        self.b_del1.Bind(wx.EVT_BUTTON, self.del1)

        # left buttons
        self.b_sel1.Bind(wx.EVT_BUTTON, self.seldir1)
        self.b_search.Bind(wx.EVT_BUTTON, self.search)  
        self.b_clearfolders.Bind(wx.EVT_BUTTON, self.clearFolders)
        self.b_clearresults.Bind(wx.EVT_BUTTON, self.clearResults) 
        self.b_quit.Bind(wx.EVT_BUTTON, self.quitApp)  

        self.clbx_results.Bind(wx.EVT_LISTBOX, self.checkSelected)
        self.clbx_results.Bind(wx.EVT_CHECKLISTBOX, self.processCheckedResults)

        self.Bind(wx.EVT_CONTEXT_MENU, self.showPopup)
        self.Bind(wx.EVT_CLOSE, self.quitApp)
        
        # TODO. for future
        #self.b_add2.Bind(wx.EVT_BUTTON, self.add2)  
        #self.b_sel2.Bind(wx.EVT_BUTTON, self.seldir2)   




    # -------------------------- Widget Actions  ------------------------- 
    # Related Methods but not directly connected to any event 
    # -------------------------------------------------------------------- 

    def cprint (self, s): 
        """Abstracts out console printing whether TextCtrl or otherwise"""
        self.t_console.AppendText(s)



    def updateStatus(self, del_flist):
        """Update search results after files have been deleted"""
           
        #self.filesel_list = []    # TODO. uncheck everything
        #self.l_status.configure(text='Clear console and hit Search again')

        self.filesel_list = []
        self.clbx_results.Set([])

        # update listing contents in place & then the listbox in search results
        for i in range(len(self.srch_results_list)): 
            f,s = self.srch_results_list[i], self.srch_sizes_list[i]

            if f.strip().startswith('##'):  
                self.srch_results_list[i] = f + '(OUTDATED)' 
            elif f.strip() in del_flist: 
                self.srch_results_list[i] = '##' + f[2:] + ' (DELETED)' 
            self.clbx_results.Append( self.srch_results_list[i] ) 


    # -------------------------- Widget Actions  -------------------------- 
    # Direct Bindings (callbacks) - respond to events 
    # -------------------------------------------------------------------- 

    def checkSelected(self, e=None):
        """Checks the corresponding boxes for selected results"""

        alist = self.srch_results_list # alias
        isel = self.clbx_results.GetSelections()
        for i in isel:
            if not alist[i].startswith('##'):
               self.clbx_results.Check(i)

        self.filesel_list = [f.strip() for f in self.clbx_results.GetCheckedStrings()]


    def processCheckedResults(self, e=None):
        """Processes the checked boxes results to figure out if they are 
        kosher choices, else deselects them"""

        # print "WTF"
        alist = self.srch_results_list # alias
        checked_nums = self.clbx_results.GetChecked()
        for i in checked_nums: 
            if alist[i].startswith('##'):
                self.clbx_results.Check(i, False)
    
        self.filesel_list = [f.strip() for f in self.clbx_results.GetCheckedStrings()]
    


    # ------------------------ Related to 5 buttons on left ------------------------ 

    def search(self, e=None):
        """Function that invokes the routine for duplicate file finding"""

        self.cprint("** 1. Creating file/directory structure **\n")

        dup_files = Dup.DuplicateFinder() 

        for p in self.ignorelist:       #TODO. Check if used
           self.cprint ("p => " + p + "\n") 
           if os.path.exists(p):
               self.cprint("   Ignoring everthing under: " + os.path.abspath(p) + "\n")
               dup_files.add2ignore(os.path.abspath(p))
        
        self.cprint( 'INFO. matched dirs (relative) to exclude:' )
        self.cprint( repr(dup_files._ignorematching) +'\n' )

        # go by what is in dirlist NOT what is displayed    # TODO
        for p in self.dirlist:
           dup_files.update(p) 
           self.cprint("   Building structure for: " + p) 

        self.cprint("\n")
        self.cprint("-- Directory structure creation complete --\n")
        self.cprint("** 2. Finding duplicates **\n")
   
        dup_table = dup_files.get_duplicates()
        self.srch_results_list, self.srch_sizes_list =  dup_files.dump_duplicates_list()

        for t in self.srch_results_list:
            self.clbx_results.Append(t)

        self.cprint("-- Duplicate listing complete --\n")
        return


    def quitApp(self, e=None):
        """Function that invokes the routine for duplicate file finding"""
        self.Destroy() 
        self.Close() 


    def clearFolders(self, e=None):
        """Clears all directory lists"""
        self.dirlist = []
        self.ignorelist = []
        self.complist = []
        self.lbx_dirs1.Set([])


    def clearResults(self, e=None):
        """Clears the serch results & console in the window"""
        self.t_console.SetValue('')
        self.clbx_results.Set([])
        self.srch_results_list = [] 
        self.srch_sizes_list = [] 



    def add1(self, e=None):
        """Adds directory entry into list of search dirs""" 

        dpath = self.t_add1.GetValue().strip('\n').strip()

        if dpath == '': 
            return
        elif dpath in self.dirlist:
            self.cprint ("Warning. Dir already added to list. %s will not be added" % (dpath))
        elif os.path.exists(dpath):
            self.dirlist.append(dpath)  # superfluous?
            self.lbx_dirs1.AppendAndEnsureVisible(dpath)
        else:
            self.cprint("Warning. Dir path does not exist. %s will not be added" % (dpath))    
 
 
    def del1(self, e=None):
        """Removes directory entry from list of search dirs""" 

        if len(self.dirlist) < 1:
            return 

        idxlist = list(self.lbx_dirs1.GetSelections())
        idxlist.sort()  

        tmplist = []    # copy over clean versions here 
        for i in range(len(self.dirlist)):
            if i in idxlist: 
                idxlist.remove(i) 
            else:    
                tmplist.append(self.dirlist[i])

        self.dirlist = tmplist
        self.lbx_dirs1.Set(tmplist)
 
 

    def seldir1(self, e=None):
       """Selects dir from ask open folder dialog box""" 
       
       ddsel = wx.DirDialog(self, "Choose a directory", style=wx.DD_DIR_MUST_EXIST) 
       if ddsel.ShowModal() != wx.ID_OK: 
           ddsel.Destroy()
           return 

       dpath = ddsel.GetPath() 
       if dpath in self.dirlist:
           self.cprint("Warning. Dir already added to list. %s will not be added" % (dpath))
           return

       self.dirlist.append(dpath)
       self.lbx_dirs1.AppendAndEnsureVisible(dpath)
       # also populate entry box with same
       self.t_add1.SetValue(dpath)
       self.t_add1.SetSelection(-1,-1) 


    # -------------------------- Widget Actions  -------------------------- 
    # Right-click/Popup Menu options
    # -------------------------------------------------------------------- 

    def showPopup(self, event):
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, pos)


    def clearSelections (self, e=None):
        """Unchecks the (checked) file selections in search results"""
         
        checked_nums = self.clbx_results.GetChecked()
        for i in checked_nums: 
            self.clbx_results.Check(i, False)
       
        self.filesel_list = []


    def openFile (self, e=None):
        """Opens selected file from console listbox"""
        # print "hello OPENFILE !!!" 
        if len(self.filesel_list) == 1:
            try:
                fname = self.filesel_list.pop(0)
                os.system('open ' + fname) # self.filesel_list.pop(0))
            except:
                self.cprint ("Could not open file %s for some reason!" % (fname))
        elif len(self.filesel_list) > 1:
            self.cprint("Cannot open multiple files. Please select ONLY one\n")


    def openFolder (self, e=None):
        """Opens enclosing folder of selected file in console listbox"""
        # print "hello OPENFOLDER !!!" 
        if len(self.filesel_list) == 1:
            dname = os.path.dirname(self.filesel_list.pop(0))
            try:
                os.system('open ' + dname) 
            except:
                self.cprint ("Could not open file %s for some reason!" % (fname))
        elif len(self.filesel_list) > 1:
            self.cprint("Cannot open multiple enclosing folders. Please select ONLY one\n")


    def deleteFile (self, e=None):
        """Deletes selected files in console listbox"""
        # print "hello DELETE selected files", self.filesel_list
        msg = "Do you want to delete the checked files?"
        yesnodlg = wx.MultiChoiceDialog(None, message=msg, caption=msg, choices=self.filesel_list, style=wx.OK|wx.CANCEL|wx.RESIZE_BORDER)
        yesnodlg.SetSelections(range(len(self.filesel_list)))

        if yesnodlg.ShowModal() != wx.ID_OK: 
            return

        final_selection = [self.filesel_list[i] for i in yesnodlg.GetSelections()]

        # for testing only 
        # for i in yesnodlg.GetSelections():
        #     print "WILL DELETE >" + self.filesel_list[i] + "<"
        # return

        for f in final_selection:
            try:
                os.unlink(f)
            except:
                self.cprint ("Could not delete file %s for some reason!" % (f))
                continue

        self.updateStatus(final_selection)



##  # TODO. ---------------------------------------------------------------------------
##  # TODO. Unused right now...
##  # TODO. ---------------------------------------------------------------------------
##    def compare(self):
##        """Function that invokes the routine for comparing directories for duplicates""" 
##
##        wprint(self.srch_log, "** 1. Creating file/directory structure **")
##        dup_files = Dup.DuplicateFinder() 
##
##        for p in self.dirlist:
##           dup_files.update(p) 
##           wprint(self.srch_log, "   Building structure for: " + p) 
##
##        wprint(self.srch_log,  "-- Directory structure creation complete --\n")
##        wprint(self.srch_log,  "** 2. Finding duplicates **\n")
##   
##        dup_table = dup_files.get_duplicates()
##
##        tmp_list, tmp_sizes = dup_files.dump_duplicates_list() 
##        wprint(self.srch_log, '\n'.join(tmp_list))
##
##        if self.comp_modevar.get() == FIND_MODE:
##            return
##        tmp = self.comp_log.get() + 'Comparing stuff'
##        self.comp_log.set(tmp) 


##     def ignoreDir (self):
##         """Ignores selected file from directory listbox"""
##         print "hello IGNORE !!!" 
##         idx = [int(i) for i in self.lbx_dirs1.curselection()][0]
##        
##         dname = self.dirlist[idx] 
##         if dname not in self.ignorelist:
##             self.ignorelist.append(dname)
##             print "self.ignorelist = ", self.ignorelist 
## 
##         self.lbx_dirs1.delete(idx)
##         self.lbx_dirs1.insert(idx, dname + ' [I]') 
## 


#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Other standard functions 
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

def guimain():
    """Calls main GUI app routine"""
    app = wx.App(False)  # redirect to terminal 
    frame = MyFrame(title="Duplicate File Finder") 
    app.MainLoop()




if __name__ == "__main__":
    #from Tkinter import *
    #pane_example() 
    guimain()


