import wx
from dupfinder_core import DuplicateFinder as Dup
from dupfinder_wx.stdpanel import StdPanel
from dupfinder_wx.cmppanel import CmpPanel
from dupfinder_wx.mainpanel import MainPanel
from version import __version__

_DEFWIDTH_ = 600

#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# MyApp class definition
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
class MyFrame(wx.Frame):
    """Top level GUI application window"""

    def __init__(self, title=None, dup_obj=None):
        wx.Frame.__init__(self, parent=None, title=title)

        # frame should always have a panel even if calls hierarchically
        # then call same 4 high level routines - init, configure, bind, display
        #  -- initUI() --
        toppanel = wx.Panel(self)
        notebook = wx.Notebook(toppanel)
        mainpanel = MainPanel(notebook, dup_obj=dup_obj)
        stdpanel = StdPanel(notebook, dup_obj=dup_obj)
        cmppanel = CmpPanel(notebook, dup_obj=dup_obj)

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


    def quitApp(self, e):   #pylint: disable-msg=W0613
        """Just about only top (frame) level funcitonality"""
        # self.Close()      # do not use Close() indiscriminately
        self.Destroy()


#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Other standard functions
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
def guimain():
    """Calls main GUI app routine"""
    dup_obj = Dup.DuplicateFinder()
    app = wx.App(False)  # redirect to terminal
    MyFrame("Duplicate File Finder", dup_obj)
    app.MainLoop()


if __name__ == "__main__":
    guimain()
