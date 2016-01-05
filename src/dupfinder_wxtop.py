#!/usr/bin/env ipython


# hierarchy
# find_duplicates_wxtop
# - _wxstdpanel 
# - _wxcmppanel 
import sys
sys.path.insert(0, '.')

import os
import os.path 
import wx
import dupfinder_wx.DuplicateFinder as Dup
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

        #  -- initUI() --
        toppanel = wx.Panel(self)      
        notebook = wx.Notebook(toppanel)
        mainpanel = MainPanel(notebook)
        stdpanel = StdPanel(notebook)
        cmppanel = CmpPanel(notebook)

        #  -- configureUI() --
        notebook.AddPage(mainpanel, "Main")
        notebook.AddPage(stdpanel, "Standard View")
        notebook.AddPage(cmppanel, "Compare View")
        mainpanel.set_stdview(stdpanel) 
        mainpanel.set_cmpview(cmppanel) 

        #  -- bindUI() --
        self.Bind(wx.EVT_BUTTON, self.quitApp, mainpanel.b_quit)
        self.Bind(wx.EVT_BUTTON, self.quitApp, stdpanel.b_quit)
        self.Bind(wx.EVT_BUTTON, self.quitApp, cmppanel.b_quit)
        self.Bind(wx.EVT_CLOSE, self.quitApp)


        #  -- displayUI() --
        mainsizer = wx.BoxSizer(wx.VERTICAL)     # break up into rows
        mainsizer.Add(notebook, 1, wx.ALL|wx.EXPAND) # , 5) # <-- ??
        # self.Layout() # we don't really need this right?
        toppanel.SetSizer(mainsizer)
        toppanel.Fit()
        self.Fit()
        self.Show() 


    def quitApp(self, e):
        """Just about only top (frame) level funcitonality"""
        # print 'event reached FRAME'
        # self.Close()      # do not use Close() indiscriminately
        self.Destroy()




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


