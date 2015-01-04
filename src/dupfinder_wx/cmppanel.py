#!/usr/bin/env ipython

'''The CmpPanel class is very similar in appearance to the StdPanel class, except
for the display of the search results which is shown in two columns rather than one.

Given the usual data structure of duplicate files to display, it breaks it down
into a 2-column format for display.
'''

# hierarchy
# dupfinder_wxtop 
# - mainpanel 
# - stdpanel 
# - cmppanel (stdpanel)


import os
import os.path 
import wx
import re
from stdpanel import StdPanel
from DuplicateFinder import get_qual, format_size 

_DEFWIDTH_ = 500
_BUTWIDTH_ = 130 

#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# CmpPanel class definition
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

class CmpPanel(StdPanel):


    # -------------------------------------------------------------------- #
    # OVERRIDE these methods for compare specific views
    # -------------------------------------------------------------------- #

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

        self.popupmenu = self.createPopupMenu()


    # -------------------------------------------------------------------- #
    def bindUI(self):               
        """Binds any mouse functions to the widgets in this section"""

        # left buttons
        self.b_clearresults.Bind(wx.EVT_BUTTON, self.onClearResults) 
        self.b_delsel.Bind(wx.EVT_BUTTON, self.onDeleteSelected)

        # selections & checkboxes 
        self.clbx1_results.Bind(wx.EVT_LISTBOX, self.processSelected)
        self.clbx1_results.Bind(wx.EVT_CHECKLISTBOX, self.processChecked)
        self.clbx2_results.Bind(wx.EVT_LISTBOX, self.processSelected)
        self.clbx2_results.Bind(wx.EVT_CHECKLISTBOX, self.processChecked)

        # popup menus
        self.Bind(wx.EVT_CONTEXT_MENU, self.showPopup)
        


    # -------------------------------------------------------------------- #
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
       

    # ------------------------ Related to buttons on left ------------------------ 
    def onClearResults(self, e=None):
        """Clears the serch results & console in the window"""
        self.t_summary.Clear()
        self.clbx1_results.Clear()
        self.clbx2_results.Clear()
        self.t_dir1.Clear()
        self.t_dir2.Clear()


    # -------------------------------------------------------------------- #
    def displayDuplicates(self): 
        """Displays duplicates of files based on instance hash 'dup_table'. dup_table
        must be provided by external panel for this panel to display""" 
    
        self.onClearResults()

        ## -- new stuff for compare mode --
        root1 = re.sub(r'(.+)[\/\\]$', r'\1', self.dirlist[0]) # strip of trailing / or \
        root2 = re.sub(r'(.+)[\/\\]$', r'\1', self.dirlist[1]) # strip of trailing / or \
        root1_list, root2_list =  [], []
        sz_list, sze_list = [], []          # size/file list and excess size/duplicate filel list
        self.t_dir1.SetValue(root1)
        self.t_dir2.SetValue(root2)

        tot_excess = 0

        ## sorted_sizes = sorted(vlist[0] for vlist in self.dup_table. TODO. easiest w/pandas

        for vlist in self.dup_table.values():

            sz_bytes = vlist[0]     # do NOT pop(0) -- modifies the hash table
            sz_excess = sz_bytes*(len(vlist)-2) 
            tot_excess += sz_excess 

            sz_f, sz_q = get_qual(sz_bytes) # size in KB, MB...
            ##sze_f, sze_q = get_qual(sz_excess)   # excess in KB, MB...
            ##sze_f = int(round(sze_f,0))

            sz_q = sz_q[0] if sz_q != '' else sz_q
            ##sze_q = sze_q[0] if sze_q != '' else sze_q

            ##sz_bytes_str = '## {} {}B x {}'.format(sz_f, sz_q, len(vlist)-1) 
            ##sz_excess_str = '({} {}B excess)'.format(sze_f, sze_q)

            ##self.clbx_results.Append('{}{:>40s}'.format(sz_bytes_str, sz_excess_str)) 
            ##for v in vlist[1:]:
            ##    self.clbx_results.Append('    {}'.format(v))

            ## -- new stuff for compare mode --
            flist1, flist2 =  [], []
            for f in vlist[1:]:
                if   f.startswith(root1): flist1.append( '   ' + f.replace(root1, '')[1:] )
                elif f.startswith(root2): flist2.append( '   ' + f.replace(root2, '')[1:] )
                else:   # try with absolute paths 
                    a_root1 = os.path.abspath(root1)
                    a_root2 = os.path.abspath(root2)
                    a_f = os.path.abspath(f)
                    if   a_f.startswith(a_root1): flist1.append( '   ' + a_f.replace(a_root1, '')[1:] )
                    elif a_f.startswith(a_root2): flist2.append( '   ' + a_f.replace(a_root2, '')[1:] )
                    else:
                        msg  = 'This is a bug in the program. The file {} must exist '.format(f)
                        msg += 'as part of either {} or {}'.format(root1, root2)
                        wx.MessageBox(msg, style=wx.ICON_EXCLAMATION)

                ## print 'DEBUG: looking at ', f
                ##print 'DEBUG:    --> flist1:', flist1, 'flist2:', flist2
                # build a pair of lists fore each hashsum - ignore empty or single-elem lists
                if (len(flist1) + len(flist2)) >= 2:  
                    root1_list.append( flist1 ) 
                    root2_list.append( flist2 )
                    sz_list.append( '{} {}B'.format(sz_f, sz_q) ) 

        # done with dup table search & build - now print
        for (flist1,flist2,sz) in zip(root1_list,root2_list,sz_list):
           # flist1 and flist2 contain lists of identical files 
           # but flist1 files may not match flist2 files 
           flist1 = sorted (flist1)
           flist2 = sorted (flist2)
           self.clbx1_results.Append('## -- {} each --\n'.format(sz)) 
           self.clbx2_results.Append('## -- {} each --\n'.format(sz)) 
           for f in flist1: self.clbx1_results.Append('    {}\n'.format(f))
           for f in flist2: self.clbx2_results.Append('    {}\n'.format(f))

        # update summary 
        self.t_summary.AppendText('Directories searched   : {}\n'.format(len(self.dirlist)) )   
        self.t_summary.AppendText('Directories excluded   : {}\n'.format(len(self.ignorelist)) )   
        self.t_summary.AppendText('Duplicate sets found   : {}\n'.format(len(self.dup_table)) )
        self.t_summary.AppendText('Total excess space used: {}\n'.format(format_size(tot_excess,0)) )
       




    # -------------------------- Widget Actions  ------------------------- #
    # Direct Bindings (callbacks) - respond to events 
    # -------------------------------------------------------------------- #
    def processSelected(self, e=None):
        """Checks the corresponding boxes for selected results"""

        # -- repeat this for the 2 checklist boxes --
        for clbx_results in  [self.clbx1_results, self.clbx2_results]:
            isel = clbx_results.GetSelections()  
            for i in isel:
                sel_str = clbx_results.GetString(i)
                if sel_str.startswith('##'):
                    clbx_results.Deselect(i)
                else:
                    chk_state = not clbx_results.IsChecked(i) # invert state on selection
                    clbx_results.Check(i, chk_state) 

        # get slections from both 
        self.filesel_list = [f.strip() for f in self.clbx1_results.GetCheckedStrings()] + \
                            [f.strip() for f in self.clbx2_results.GetCheckedStrings()] 
        

    # -------------------------------------------------------------------- #
    def processChecked(self, e=None):
        """Processes the checked boxes to figure out if they are 
        kosher choices, else deselects them"""

        # -- repeat this for the 2 checklist boxes --
        for clbx_results in  [self.clbx1_results, self.clbx2_results]:
            checked_nums = clbx_results.GetChecked()
            for i in checked_nums: 
                sel_str = clbx_results.GetString(i)
                if sel_str.startswith('##'):
                    clbx_results.Check(i, False)

        # get slections from both 
        self.filesel_list = [f.strip() for f in self.clbx1_results.GetCheckedStrings()] + \
                            [f.strip() for f in self.clbx2_results.GetCheckedStrings()] 
    
    # -------------------------------------------------------------------- #
    def clearSelections (self, e=None):
        """Unchecks the (checked) file selections in search results"""
         
        checked_nums = self.clbx1_results.GetChecked()
        for i in checked_nums: self.clbx1_results.Check(i, False)

        checked_nums = self.clbx2_results.GetChecked()
        for i in checked_nums: self.clbx2_results.Check(i, False)

        self.filesel_list = []



#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Other standard functions 
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>



