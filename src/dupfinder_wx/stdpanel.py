#!/usr/bin/env ipython

'''The StdPanel class basically displays the search results, and has additional
functionality to delete duplicates. It takes in data from the main panel as a
data structure of duplicate files to display and breaks it down appropriately.

However, it does not need any calls to DuplicateFinder class/methods. (There is
a generic function that is used though...)
'''

#pylint: disable=W0511
#pylint: disable=W0702
#pylint: disable=W0613


# hierarchy
# dupfinder_wxtop
# - mainpanel
# - stdpanel
# - cmppanel (stdpanel)

import os
import os.path
import wx

_DEFWIDTH_ = 500
_BUTWIDTH_ = 130


#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# StdPanel class definition
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

class StdPanel(wx.Panel):
    def __init__(self, parent, dup_obj=None):
        wx.Panel.__init__(self, parent=parent)

        # variables need for non-GUI execution
        self.dup_obj = dup_obj

        # These 3 are passed in from mainpanel & then maintained locally
        self.dirlist = []               # list of directories to search
        self.ignorelist = []            # list of directories to ignore
        self.dup_table = {}             # Raw table { 'md5sum1' : [sz, file1, file2, file3, ...], ... }

        # This list is generated & maintained purely in this panel
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

        self.popupmenu = self.createPopupMenu()



    # -------------------------------------------------------------------- #
    def configureUI(self):
        """Performs additional configuration of GUI beyond just simple initialization,
        especially when related to geometries"""

        self.sb_status.SetStatusText('Right click for more options')



    # -------------------------------------------------------------------- #
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

    # -------------------------------------------------------------------- #
    def createPopupMenu(self):
        item_names = ['Delete', 'Clear Selections', 'Open Enclosing Folder', 'Open File']
        item_funcs = [self.onDeleteSelected, self.clearSelections, self.openFolder, self.openFile]

        pmenu = wx.Menu()

        for (iname,ifunc) in zip(item_names,item_funcs):
            item = pmenu.Append(-1, iname)
            self.Bind(wx.EVT_MENU, ifunc, item)
        return pmenu

    # -------------------------------------------------------------------- #
    def bindUI(self):
        """Binds any mouse functions to the widgets in this section"""

        # left buttons
        self.b_clearresults.Bind(wx.EVT_BUTTON, self.onClearResults)
        self.b_delsel.Bind(wx.EVT_BUTTON, self.onDeleteSelected)

        # selections & checkboxes
        self.clbx_results.Bind(wx.EVT_LISTBOX, self.processSelected)
        self.clbx_results.Bind(wx.EVT_CHECKLISTBOX, self.processChecked)

        # popup menus
        self.Bind(wx.EVT_CONTEXT_MENU, self.showPopup)


    # -------------------------- Widget Actions  -------------------------
    # Related Methods but not directly connected to any event
    # --------------------------------------------------------------------



    def updateStatus(self, del_flist):
        """Update search results after files have been deleted"""

        # THIS IS THE NEW METHOD - appears to be EVEN slower than original ??
        #del_set = set(del_flist)

#       new_dict = {}
#       for k, vlist in self.dup_table.items():
#           if len(del_set) == 0:
#               break
#           tmplist = []
#           for v in vlist[1:]:
#               if v in del_set:
#                   del_set.remove(v)
#               else:
#                   tmplist.append(v)
#           if len(tmplist) > 1:
#               tmplist.insert(0, vlist[0])
#               new_dict[k] = tmplist

#       self.dup_table = new_dict

        # THIS IS THE ORIGINAL METHOD - pretty slow
        del_set = set(del_flist)

        for k, vlist in self.dup_table.items():
            vset = set(vlist)
            for v in del_set.intersection(vset):
                ## print 'Removing ', v
                vlist.remove(v)
            if len(vlist) < 3:
                del self.dup_table[k]
            else:
                self.dup_table[k] = vlist

        #for k, vlist in new_dict.items():       print 'NEW {} -> {}'.format(k, vlist)
        #for k, vlist in self.dup_table.items(): print 'DUP {} -> {}'.format(k, vlist)
        self.displayDuplicates()


    # -------------------------------------------------------------------- #
    def displayDuplicates(self):
        """Displays duplicates of files based on instance hash 'dup_table'. dup_table
        must be provided by external panel for this panel to display"""

        #TODO. For future -- TREE VIEW -- how to keep tree & dup_table in sync?
        #
        #sample_data = { 25: ['abc', 'def'], 28: ['xyz'] }
        #tree = wx.TreeCtrl(self, size=(600, 300))
        #root_id = tree.AddRoot('Sample Data')
        #for k, vlist in sample_data.items():
        #    child_id = tree.AppendItem(root_id, str(k))
        #    for v in vlist:
        #        tree.AppendItem(child_id, v)

        self.onClearResults()

        tot_excess = 0

        sorted_list = sorted( self.dup_table.values(), key=lambda x: x[0], reverse=True )

        # for k,vlist in self.dup_table.items():
        for vlist in sorted_list:
            sz_bytes = vlist[0]     # do NOT pop(0) -- modifies the hash table
            sz_excess = sz_bytes*(len(vlist)-2)
            tot_excess += sz_excess

            sz_f, sz_q = self.dup_obj.get_qual(sz_bytes) # size in KB, MB...
            sze_f, sze_q = self.dup_obj.get_qual(sz_excess)   # excess in KB, MB...
            sze_f = int(round(sze_f,0))

            sz_q = sz_q[0] if sz_q != '' else sz_q
            sze_q = sze_q[0] if sze_q != '' else sze_q

            sz_bytes_str = '## {} {}B x {}'.format(sz_f, sz_q, len(vlist)-1)
            sz_excess_str = '({} {}B excess)'.format(sze_f, sze_q)

            self.clbx_results.Append('{}{:>40s}'.format(sz_bytes_str, sz_excess_str))
            for v in vlist[1:]:
                self.clbx_results.Append('    {}'.format(v))

        # update summary
        self.t_summary.AppendText('Directories searched        : {}\n'.format(len(self.dirlist)))
        self.t_summary.AppendText('Directories excluded        : {}\n'.format(len(self.ignorelist)))
        self.t_summary.AppendText('Duplicate sets found        : {}\n'.format(len(self.dup_table)))
        self.t_summary.AppendText('Total excess space used     : {}\n'.format(self.dup_obj.format_size(tot_excess,0)))
        self.t_summary.AppendText('Files selected for deletion : {}\n'.format(len(self.filesel_list)))


    # -------------------------- Widget Actions  ------------------------- #
    # Direct Bindings (callbacks) - respond to events
    # -------------------------------------------------------------------- #
    def processSelected(self, e=None):
        """Checks the corresponding boxes for selected results"""

        isel = self.clbx_results.GetSelections()
        for i in isel:
            sel_str = self.clbx_results.GetString(i)
            if sel_str.startswith('##'):
                self.clbx_results.Deselect(i)
            else:
                #self.clbx_results.Check(i)
                chk_state = not self.clbx_results.IsChecked(i) # invert state on selection
                self.clbx_results.Check(i, chk_state)

        self.filesel_list = [f.strip() for f in self.clbx_results.GetCheckedStrings()]
        ## m_dlg = wx.MessageBox('you selected  ' + '\n'.join(self.filesel_list), caption="Message", style=wx.OK)


    # -------------------------------------------------------------------- #
    def processChecked(self, e=None):
        """Processes the checked boxes to figure out if they are
        kosher choices, else deselects them"""

        checked_nums = self.clbx_results.GetChecked()
        for i in checked_nums:
            sel_str = self.clbx_results.GetString(i)
            if sel_str.startswith('##'):
                self.clbx_results.Check(i, False)

        self.filesel_list = [f.strip() for f in self.clbx_results.GetCheckedStrings()]
        ## m_dlg = wx.MessageBox('you selected  ' + '\n'.join(self.filesel_list), caption="Message", style=wx.OK)


    # ------------------------ Related to buttons on left ------------------------
    def onClearResults(self, e=None):
        """Clears the serch results & console in the window"""
        self.t_summary.Clear()
        self.clbx_results.Clear()


    # -------------------------- Widget Actions  --------------------------
    # Right-click/Popup Menu options
    # --------------------------------------------------------------------
    def showPopup(self, event):
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, pos)

    # -------------------------------------------------------------------- #
    def clearSelections (self, e=None):
        """Unchecks the (checked) file selections in search results"""

        checked_nums = self.clbx_results.GetChecked()
        for i in checked_nums:
            self.clbx_results.Check(i, False)
        self.filesel_list = []

    # -------------------------------------------------------------------- #
    def openFile (self, e=None):
        """Opens selected file from console listbox"""
        # print "hello OPENFILE !!!"
        if len(self.filesel_list) == 1:
            try:
                fname = self.filesel_list.pop(0)
                os.system('open ' + fname) # self.filesel_list.pop(0))
            except:
                wx.MessageBox("Could not open file %s for some reason!" % (fname))
        elif len(self.filesel_list) > 1:
            wx.MessageBox("Cannot open multiple files. Please select ONLY one\n")

    # -------------------------------------------------------------------- #
    def openFolder (self, e=None):
        """Opens enclosing folder of selected file in console listbox"""
        # print "hello OPENFOLDER !!!"
        if len(self.filesel_list) == 1:
            dname = os.path.dirname(self.filesel_list.pop(0))
            try:
                os.system('open ' + dname)
            except:
                wx.MessageBox ("Could not open file {} for some reason!".format(dname))
        elif len(self.filesel_list) > 1:
            wx.MessageBox("Cannot open multiple enclosing folders. Please select ONLY one\n")


    # -------------------------------------------------------------------- #
    def onDeleteSelected (self, e=None):
        """Deletes selected files in console listbox. Has option to not delete all originally
        selected files"""

        # print "hello DELETE selected files", self.filesel_list
        msg = "Do you want to delete the checked files?"
        yesnodlg = wx.MultiChoiceDialog(None, message=msg, caption="Delete Selected", choices=self.filesel_list,
            style=wx.OK|wx.CANCEL|wx.RESIZE_BORDER)
        yesnodlg.SetSelections(range(len(self.filesel_list)))

        if yesnodlg.ShowModal() != wx.ID_OK:
            return

        final_selection = [self.filesel_list[i] for i in yesnodlg.GetSelections()]

        deleted_files = final_selection[:] # get copy

        for f in final_selection:
            try:
                os.unlink(f)
            except:
                msg = 'Could not delete file {} for some reason!'.format(f)
                wx.MessageBox(msg, caption="WARNING", style=wx.OK)
                deleted_files.remove(f)
                continue

        yesnodlg.Destroy()

        self.filesel_list = []      # reset all selections
        self.updateStatus(deleted_files)




#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Other standard functions
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
