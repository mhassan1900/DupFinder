#!/usr/bin/env ipython

'''The CmpPanel class is very similar in appearance to the StdPanel class, except
for the display of the search results which is shown in two columns rather than one.

Given the usual data structure of duplicate files to display, it breaks it down
into a 2-column format for display.
'''


# hierarchy
# find_duplicates_wxtop
# - mainpanel 
# - stdpanel 
# - cmppanel 


import os
import os.path 
import wx
from stdpanel import StdPanel

_DEFWIDTH_ = 600

#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# CmpPanel class definition
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

class CmpPanel(StdPanel):

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

        # 2 new additional widgets 
        self.t_dir1 = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.t_dir2 = wx.TextCtrl(self, style=wx.TE_READONLY)

        #  changed one column to two for search results 
        self.clbx1_results = wx.CheckListBox(self, style=wx.HSCROLL|wx.LB_NEEDED_SB|wx.LB_EXTENDED, 
            choices=[], size=(_DEFWIDTH_/2,300))
        self.clbx2_results = wx.CheckListBox(self, style=wx.HSCROLL|wx.LB_NEEDED_SB|wx.LB_EXTENDED, 
            choices=[], size=(_DEFWIDTH_/2,300))

        self.sb_status = wx.StatusBar(self)

##      self.popupmenu = self.createPopupMenu()


    def clearResults(self,e=None):
        pass

    def bindUI(self):               
        """Binds any mouse functions to the widgets in this section"""

        # left buttons
        self.b_clearresults.Bind(wx.EVT_BUTTON, self.clearResults) 

##      self.clbx_results.Bind(wx.EVT_LISTBOX, self.checkSelected)
##      self.clbx_results.Bind(wx.EVT_CHECKLISTBOX, self.processCheckedResults)

        self.Bind(wx.EVT_CONTEXT_MENU, self.showPopup)
 

    def displayUI(self):
        """Actually displays the different widgets of the UI. Has most of the grid 
        packing rules in here""" 

        mainsizer = wx.BoxSizer(wx.VERTICAL)     # break up into rows
        hsizer2   = wx.BoxSizer(wx.HORIZONTAL)   # for row 2
        vsizer2l  = wx.BoxSizer(wx.VERTICAL)     # for row 2.L
        vsizer2r  = wx.BoxSizer(wx.VERTICAL)     # for row 2.R
        hsizer3   = wx.BoxSizer(wx.HORIZONTAL)   # for row 3
        vsizer3l  = wx.BoxSizer(wx.VERTICAL)     # for row 3.L
        vsizer3r  = wx.BoxSizer(wx.VERTICAL)     # for row 3.R


        # row2, left - buttons 
        dummy_label = wx.StaticText(self, label='')
        vsizer2l.Add(dummy_label)
        buttons = [self.b_clearresults, self.b_delsel, self.b_quit] 
        for b in buttons: vsizer2l.Add(b, 0, flag=wx.EXPAND)  

        # row2, right side 
        vsizer2r.Add(self.st_summary, flag=wx.EXPAND)
        vsizer2r.Add(self.t_summary, flag=wx.EXPAND)

        # vsizer2r.RecalcSizes()

        # row2
        hsizer2.Add(vsizer2l, 0, flag=wx.EXPAND)
        hsizer2.Add(vsizer2r, 1, flag=wx.EXPAND)


        # row3 left
        vsizer3l.Add(self.t_dir1, flag=wx.EXPAND)
        vsizer3l.Add(self.clbx1_results, 1, flag=wx.EXPAND)

        # row3 right
        vsizer3r.Add(self.t_dir2, flag=wx.EXPAND)
        vsizer3r.Add(self.clbx2_results, 1, flag=wx.EXPAND)

        # row3
        hsizer3.Add(vsizer3l, 1, flag=wx.EXPAND)
        hsizer3.Add(vsizer3r, 1, flag=wx.EXPAND)

        # now add all the rows/sizers
        mainsizer.Add(hsizer2, 0, flag=wx.EXPAND) 
        mainsizer.AddSpacer(5)
        mainsizer.Add(self.st_results, 0)
        mainsizer.Add(hsizer3, 1, flag=wx.EXPAND)
        mainsizer.Add(self.sb_status, 0, flag=wx.EXPAND)
        self.SetSizer(mainsizer)
        self.Fit()
       



#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Other standard functions 
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>



