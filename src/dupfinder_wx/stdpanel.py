#!/usr/bin/env ipython

'''The StdPanel class basically displays the search results, and has additional 
functionality to delete duplicates. It takes in data from the main panel as a 
data structure of duplicate files to display and breaks it down appropriately.
'''


# hierarchy
# find_duplicates_wxtop
# - mainpanel 
# - stdpanel 
# - cmppanel 


import os
import os.path 
import wx

_DEFWIDTH_ = 500
_BUTWIDTH_ = 130 

#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# CmpPanel class definition
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

class StdPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        # variables need for non-GUI execution
        self.dirlist = []               # list of directories to search
        self.ignorelist = []            # list of directories to ignore
        self.srch_results_list = []     # list of names in search results (includes comments)
        self.srch_sizes_list = []       # list of sizes from search results
        self.filesel_list = []          # list of (checked) selections from search results

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

        self.b_clearresults = wx.Button(self, label='Clear Results')
        self.b_delsel = wx.Button(self, label='Delete Selections')
        self.b_quit = wx.Button(self, label='Quit')

        self.st_summary = wx.StaticText(self, label='Summary') 
        self.t_summary = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.VSCROLL|wx.TE_READONLY, 
                size=(_DEFWIDTH_,100))

        self.st_results = wx.StaticText(self, label='Search results') 
        self.clbx_results = wx.CheckListBox(self, style=wx.HSCROLL|wx.LB_NEEDED_SB|wx.LB_EXTENDED, 
            choices=[], size=(_DEFWIDTH_,300))

        self.sb_status = wx.StatusBar(self)

##      self.popupmenu = self.createPopupMenu()



    def configureUI(self):
        """Performs additional configuration of GUI beyond just simple initialization, 
        especially when related to geometries""" 
        
        self.sb_status.SetStatusText('Right click for more options') 



    def displayUI(self):
        """Actually displays the different widgets of the UI. Has most of the grid 
        packing rules in here""" 

        mainsizer = wx.BoxSizer(wx.VERTICAL)     # break up into rows
        hsizer2   = wx.BoxSizer(wx.HORIZONTAL)   # for row 2
        vsizer2l  = wx.BoxSizer(wx.VERTICAL)     # for row 2.L
        vsizer2r  = wx.BoxSizer(wx.VERTICAL)     # for row 2.R

        # row2, right side 
        vsizer2r.Add(self.st_summary, flag=wx.EXPAND)
        vsizer2r.Add(self.t_summary, flag=wx.EXPAND)

        # row2, left - buttons 
        dummy_label = wx.StaticText(self, label='')
        vsizer2l.Add(dummy_label)
        buttons = [self.b_clearresults, self.b_delsel, self.b_quit] 
        for b in buttons: vsizer2l.Add(b, 0, flag=wx.EXPAND)  

        # vsizer2r.RecalcSizes()

        # row2
        hsizer2.Add(vsizer2l, 0, flag=wx.EXPAND)
        hsizer2.Add(vsizer2r, 1, flag=wx.EXPAND)

        # now add all the rows/sizers
        mainsizer.Add(hsizer2, 0, flag=wx.EXPAND) 
        mainsizer.AddSpacer(5)
        mainsizer.Add(self.st_results, 0)
        mainsizer.Add(self.clbx_results, 1, flag=wx.EXPAND)
        mainsizer.Add(self.sb_status, 0, flag=wx.EXPAND)
        self.SetSizer(mainsizer)
        self.Fit()
       


##    def createPopupMenu(self):               
##        item_names = ['Delete', 'Clear Selections', 'Open Enclosing Folder', 'Open File'] 
##        item_funcs = [self.deleteFile, self.clearSelections, self.openFolder, self.openFile] 
##
##        pmenu = wx.Menu()
##
##        for (iname,ifunc) in zip(item_names,item_funcs):
##            item = pmenu.Append(-1, iname)
##            self.Bind(wx.EVT_MENU, ifunc, item)
##    
##        return pmenu



    def bindUI(self):               
        """Binds any mouse functions to the widgets in this section"""

        # left buttons
##        self.b_clearresults.Bind(wx.EVT_BUTTON, self.clearResults) 

##  TODO. Need these 
##        self.clbx_results.Bind(wx.EVT_LISTBOX, self.checkSelected)
##        self.clbx_results.Bind(wx.EVT_CHECKLISTBOX, self.processCheckedResults)

        self.Bind(wx.EVT_CONTEXT_MENU, self.showPopup)
        


## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
## TEMP - DUMMY FUNCTIONS TO GET GOING...    
## <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    def clearResults(self, e=None):
        pass

    def checkSelected(self, e=None):
        pass

    def processCheckedResults(self, e=None):
        pass

    def processCheckedResults(self, e=None):
        pass

    def showPopup(self, event):
        pass


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

##     def checkSelected(self, e=None):
##         """Checks the corresponding boxes for selected results"""
## 
##         alist = self.srch_results_list # alias
##         isel = self.clbx_results.GetSelections()
##         for i in isel:
##             if not alist[i].startswith('##'):
##                self.clbx_results.Check(i)
## 
##         self.filesel_list = [f.strip() for f in self.clbx_results.GetCheckedStrings()]
## 
## 
##     def processCheckedResults(self, e=None):
##         """Processes the checked boxes results to figure out if they are 
##         kosher choices, else deselects them"""
## 
##         # print "WTF"
##         alist = self.srch_results_list # alias
##         checked_nums = self.clbx_results.GetChecked()
##         for i in checked_nums: 
##             if alist[i].startswith('##'):
##                 self.clbx_results.Check(i, False)
##     
##         self.filesel_list = [f.strip() for f in self.clbx_results.GetCheckedStrings()]
##     
## 

##     # ------------------------ Related to 5 buttons on left ------------------------ 
## 
## 
## 
##     def clearResults(self, e=None):
##         """Clears the serch results & console in the window"""
##         self.t_console.SetValue('')
##         self.clbx_results.Set([])
##         self.srch_results_list = [] 
##         self.srch_sizes_list = [] 
## 
## 

    # -------------------------- Widget Actions  -------------------------- 
    # Right-click/Popup Menu options
    # -------------------------------------------------------------------- 

##     def showPopup(self, event):
##         pos = event.GetPosition()
##         pos = self.ScreenToClient(pos)
##         self.PopupMenu(self.popupmenu, pos)
## 
## 
##     def clearSelections (self, e=None):
##         """Unchecks the (checked) file selections in search results"""
##          
##         checked_nums = self.clbx_results.GetChecked()
##         for i in checked_nums: 
##             self.clbx_results.Check(i, False)
##        
##         self.filesel_list = []
## 
## 
##     def openFile (self, e=None):
##         """Opens selected file from console listbox"""
##         # print "hello OPENFILE !!!" 
##         if len(self.filesel_list) == 1:
##             try:
##                 fname = self.filesel_list.pop(0)
##                 os.system('open ' + fname) # self.filesel_list.pop(0))
##             except:
##                 self.cprint ("Could not open file %s for some reason!" % (fname))
##         elif len(self.filesel_list) > 1:
##             self.cprint("Cannot open multiple files. Please select ONLY one\n")
## 
## 
##     def openFolder (self, e=None):
##         """Opens enclosing folder of selected file in console listbox"""
##         # print "hello OPENFOLDER !!!" 
##         if len(self.filesel_list) == 1:
##             dname = os.path.dirname(self.filesel_list.pop(0))
##             try:
##                 os.system('open ' + dname) 
##             except:
##                 self.cprint ("Could not open file %s for some reason!" % (fname))
##         elif len(self.filesel_list) > 1:
##             self.cprint("Cannot open multiple enclosing folders. Please select ONLY one\n")
## 
## 
##     def deleteFile (self, e=None):
##         """Deletes selected files in console listbox"""
##         # print "hello DELETE selected files", self.filesel_list
##         msg = "Do you want to delete the checked files?"
##         yesnodlg = wx.MultiChoiceDialog(None, message=msg, caption=msg, choices=self.filesel_list, style=wx.OK|wx.CANCEL|wx.RESIZE_BORDER)
##         yesnodlg.SetSelections(range(len(self.filesel_list)))
## 
##         if yesnodlg.ShowModal() != wx.ID_OK: 
##             return
## 
##         final_selection = [self.filesel_list[i] for i in yesnodlg.GetSelections()]
## 
##         # for testing only 
##         # for i in yesnodlg.GetSelections():
##         #     print "WILL DELETE >" + self.filesel_list[i] + "<"
##         # return
## 
##         for f in final_selection:
##             try:
##                 os.unlink(f)
##             except:
##                 self.cprint ("Could not delete file %s for some reason!" % (f))
##                 continue
## 
##         self.updateStatus(final_selection)
## 
## 


#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Other standard functions 
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>



