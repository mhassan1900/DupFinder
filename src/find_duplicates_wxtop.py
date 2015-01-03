#!/usr/bin/env ipython


# hierarchy
# find_duplicates_wxtop
# - _wxstdpanel 
# - _wxcmppanel 


import os
import os.path 
import DuplicateFinder as Dup
import wx
from dupfinder_wx.stdpanel import StdPanel  
from dupfinder_wx.cmppanel import CmpPanel
from dupfinder_wx.mainpanel import MainPanel  


_DEFWIDTH_ = 600

#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# MyApp class definition
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


class MyFrame(wx.Frame):
    """Top level GUI application window"""

    def __init__(self, title=None):
        wx.Frame.__init__(self, parent=None, title=title)

        # frame should always have a panel even if calls hierarchically
        # then call same 4 high level routines - init, configure, bind, display

        #  initUI() -->
        toppanel = wx.Panel(self)      
        notebook = wx.Notebook(toppanel)
        mainpanel = MainPanel(notebook)
        stdpanel = StdPanel(notebook)
        cmppanel = CmpPanel(notebook)

        #  configureUI() -->
        notebook.AddPage(mainpanel, "Main")
        notebook.AddPage(stdpanel, "Standard View")
        notebook.AddPage(cmppanel, "Compare View")

        #  bundUI() -->

        #  displayUI() -->
        mainsizer = wx.BoxSizer(wx.VERTICAL)     # break up into rows
        mainsizer.Add(notebook, 1, wx.ALL|wx.EXPAND) # , 5) # <-- ??
        # self.Layout() # we don't really need this right?
        toppanel.SetSizer(mainsizer)
        toppanel.Fit()
        self.Fit()
        self.Show() 







#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Other standard functions 
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

def guimain():
    """Calls main GUI app routine"""
    app = wx.App(False)  # redirect to terminal 
    frame = MyFrame(title="Duplicate File Finder") 
    app.MainLoop()



if __name__ == "__main__":
    guimain()


