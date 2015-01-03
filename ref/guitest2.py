#!/usr/bin/env ipython


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

        #  -- initUI() --
        toppanel = wx.Panel(self)      
        b_quit = wx.Button(self, label='Quit')

        sample_data = { 25: ['abc', 'def'], 28: ['xyz'] }

        tree = wx.TreeCtrl(self, size=(600, 300))
        root_id = tree.AddRoot('Sample Data')
        for k, vlist in sample_data.items():
            child_id = tree.AppendItem(root_id, str(k)) 
            for v in vlist:
                tree.AppendItem(child_id, v) 

        # self.AddTreeNodes(root, data.tree)

        #  -- configureUI() --


        #  -- bindUI() --
        self.Bind(wx.EVT_BUTTON, self.quitApp, b_quit)
        self.Bind(wx.EVT_CLOSE, self.quitApp)



        #  -- displayUI() --
        mainsizer = wx.BoxSizer(wx.VERTICAL)     # break up into rows
        mainsizer.Add(b_quit) # , 0, wx.ALL|wx.EXPAND) # , 5) # <-- ?A
        mainsizer.Add(tree, 1, wx.EXPAND)
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
    frame = MyFrame(title="GUI TESTER") 
    app.MainLoop()


if __name__ == "__main__":
    guimain()


