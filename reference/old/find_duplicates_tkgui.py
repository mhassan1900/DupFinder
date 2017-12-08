#!/usr/bin/env ipython

import os
import os.path 
import Tkinter as Tk
from Tkinter import RIGHT, LEFT, END, Y, N, S, E, W
from tkFileDialog import askdirectory, askopenfilename
from tkMessageBox import askyesno

import DuplicateFinder as Dup


#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# MyApp class definition
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

# Global Constants
COMP_MODE = 2
FIND_MODE = 1

MAX_BUF_LINES = 10
MAX_BUF_SIZE = 1000
TOL_SIZE = 3*80 
TOL_LINES = 3 



class MyApp(Tk.Tk):
    """Master application window for Duplicate File Finder"""

    def __init__(self, parent=None):
        """Initialization of GUI widgets and methods"""
        Tk.Tk.__init__(self, parent) 

        # variables for GUI execution
        self.parent = parent
        self.comp_modevar = Tk.IntVar()     # radio button choice 1, or 2
        self.srch_log = Tk.StringVar()      # console for search 
        self.comp_log = Tk.StringVar()      # console for compare 

        # variables need for non-GUI execution
        self.dirlist = []
        self.complist = []
        self.ignorelist = []

        self.srch_log_list = []
        self.comp_log_list = []
        self.srch_sizes_list = []

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

        v = self.comp_modevar 
        self.rb_finddup = Tk.Radiobutton(self, text='Find Duplicates', 
            variable=v, value=FIND_MODE)    # TODO. ,command=self.set_find_mode)
            # variable=v, value=FIND_MODE,command=lambda: self.comp_modevar.set(FIND_MODE) )
        self.rb_compare = Tk.Radiobutton(self, text='Compare Folders', 
            variable=v, value=COMP_MODE, command=self.set_comp_mode) 
            # command=lambda: self.comp_modevar.set(COMP_MODE) )

        # Selection buttons (after selection)
        self.b_add1 = Tk.Button(self, text='+', command=self.add1)
        self.b_add2 = Tk.Button(self, text='+', command=self.add2)

        self.b_sel1 = Tk.Button(self, text='Select Folder(s)',  command=self.seldir1)
        self.b_sel2 = Tk.Button(self, text='Select Folder (Compare)', command=self.seldir2)

        self.e_add1 = Tk.Entry(self) 
        self.e_add2 = Tk.Entry(self) 


        self.lbfm1 = Tk.LabelFrame(self, text="Folders to search\n", padx=0, pady=0)
        self.lbfm2 = Tk.LabelFrame(self, text="Folders to compare\n")

        self.sb_dirs1 = Tk.Scrollbar(self.lbfm1, orient=Tk.VERTICAL)
        self.lbx_dirs1 = Tk.Listbox(self.lbfm1, yscrollcommand=self.sb_dirs1.set)


        # Action buttons (after selection)
        self.b_search = Tk.Button(self, text='Search', command=self.search)
        self.b_cleardir = Tk.Button(self, text='Clear Folders', command=self.clearDir)
        self.b_clearlog = Tk.Button(self, text='Clear Console', command=self.clearLog)
        self.b_quit = Tk.Button (self, text='Quit', command=self.quit)
       
        # Display related 
        self.lbfm_console1 = Tk.LabelFrame(self, text='Search Results', padx=0, pady=0)
        self.lbfm_console2 = Tk.LabelFrame(self, text='Compare Results', padx=0, pady=0)
        self.sb_console1 = Tk.Scrollbar(self.lbfm_console1, orient=Tk.VERTICAL)
        self.lbx_console1 = Tk.Listbox(self.lbfm_console1, yscrollcommand=self.sb_console1.set,
                                selectmode=Tk.EXTENDED) 

        self.lbx_console2 = Tk.Listbox(self.lbfm_console2) 

        self.m_console1 = Tk.Menu(self) 
        self.m_dirs1 = Tk.Menu(self) 

        # Popup menus
        self.m_dirs1.add_command(label='Ignore', command=self.ignoreDir)

        self.m_console1.add_command(label='Open', command=self.openFile)
        self.m_console1.add_command(label='Open Enclosing Folder', command=self.openFolder)
        self.m_console1.add_command(label='Delete', command=self.deleteFile)

        # Logging messages
        self.lbfm_log = Tk.LabelFrame(self, padx=0, pady=0)
        self.t_msg = Tk.Text(self.lbfm_log, borderwidth=1)  # Text boxes ONLY have horizontal scrolling!!!
        self.l_status = Tk.Label(self, bg='lightgray',   
            text="Steps: [1] Select folder(s) [2] Hit Search [3] Left mouse to select files, Right click to take action") 



    def configureUI(self):
        """Performs additional configuration of GUI beyond just simple initialization, 
        especially when related to geometries""" 

        self.rb_finddup.select()
        self.comp_modevar.set(FIND_MODE)    # not in compare mode 

        self.e_add1.insert(0, 'You may type in folder name directly to add (+)') 
        self.e_add1.select_range(0, END)
        self.e_add1.focus_set()

        self.e_add2.insert(0, 'You may type in folder name directly to add (+)') 
        self.e_add2.select_range(0, END)
        # self.e_add2.focus_set()

        self.lbx_dirs1.configure(height=4, width=60)
        self.sb_dirs1.configure(command=self.lbx_dirs1.yview)

        #self.b_search.configure(anchor='nw')
        #self.b_cleardir.configure(anchor='n')
        #self.b_clearlog.configure(anchor='n')
        #self.b_quit.configure(anchor='ne')

        self.lbx_console1.configure(height=20, width=75) # , anchor='nw')
        self.sb_console1.configure(command=self.lbx_console1.yview)

        self.lbx_console2.configure(height=20, width=75) # , anchor='ne')

        self.t_msg.configure(height=4, width=90)



    def displayUI(self):
        """Actually displays the different widgets of the UI. Has most of the grid 
        packing rules in here""" 

        self.rb_finddup.grid(column=1, row=0, sticky='NW') 
        self.rb_compare.grid(column=3, row=0, sticky='NE') 

        self.b_sel1.grid(row=1, column=0, sticky='EW') 
        self.e_add1.grid(row=1, column=1, columnspan=3, sticky='EW')
        self.b_add1.grid(row=1, column=4, sticky='NE') 


        self.b_search.grid  (row=2, column=0, sticky='EW') 
        self.b_cleardir.grid(row=3, column=0, sticky='EW')
        self.b_clearlog.grid(row=4, column=0, sticky='EW') 
        self.b_quit.grid    (row=5, column=0, sticky='EW') 

        # Replace this later on
        # self.set_find_mode() # TODO
        # ---------------------------------

        self.comp_modevar.set(FIND_MODE) 
        self.b_search.configure(text='Search', command=self.search)

        self.lbfm1.grid(row=2, column=1, columnspan=4, rowspan=4, sticky='EW') 
        self.lbx_dirs1.grid(row=0, column=0, columnspan=4, rowspan=4, sticky='NSEW') 
        self.sb_dirs1.grid  (row=0, column=4, sticky='NS') # , sticky=N+S)
        self.lbfm_console1.grid(row=8, column= 0, columnspan=5, sticky='EW') 
        self.lbx_console1.grid(row=9, column=0, columnspan=5, sticky='EW') 
        self.sb_console1.grid(row=9, column=5, sticky='NS') 
        # ---------------------------------

        self.lbfm_log.grid(row=10, column= 0, columnspan=5, sticky='NSEW') 
        self.t_msg.grid(row=0, column=0, columnspan=5, sticky='NSEW')
        self.l_status.grid(row=11, column=0, columnspan=5, sticky='NSEW')

        if self.comp_modevar.get() == COMP_MODE:
            self.set_comp_mode()

        # Needed so that they are the last things
        col_count, row_count = self.grid_size()
       
        

    def set_find_mode(self):
        self.comp_modevar.set(FIND_MODE) 
        self.b_search.configure(text='Search', command=self.search)
        # forget/remove the other stuff
        self.b_add2.grid_forget()
        self.e_add2.grid_forget()
        self.b_sel2.grid_forget() 
        self.lbfm2.grid_forget()
        self.label_dirs2.grid_forget()
        self.lbfm_console2.grid_forget()
        self.lbx_console2.grid_forget()

        # determine current stuff 
        self.comp_modevar.set(FIND_MODE) 
        self.b_search.configure(text='Search', command=self.search)

        self.lbfm1.grid(row=2, column=1, columnspan=4, rowspan=4, sticky='EW') 
        self.lbx_dirs1.grid(row=0, column=0, columnspan=4, rowspan=4, sticky='NSEW') 
        self.sb_dirs1.grid  (row=0, column=4, sticky='NS') 
        self.lbfm_console1.grid(row=8, column= 0, columnspan=5, sticky='EW') 
        self.lbx_console1.grid(row=9, column=0, columnspan=5, sticky='EW') 
        self.t_msg.grid(row=10, column=0, columnspan=5, sticky='NSEW')



    def set_comp_mode(self):
        self.comp_modevar.set(FIND_MODE) 
        return

        # ** TODO. Ignore all this stuff for now ** 
        self.comp_modevar.set(COMP_MODE) 
        self.b_search.configure(text='Compare', command=self.compare)
        # add the other stuff
        self.b_sel2.grid(row=2, column=0, sticky='EW') 
        self.e_add2.grid(row=2, column=1, columnspan=3, sticky='EW') 
        self.b_add2.grid(row=2, column=4, sticky='EW') 
        self.lbfm2.grid(row=3, column=2, columnspan=2, sticky='EW') 
        self.lbfm_console2.grid(row=8, column= 2, columnspan=2, sticky='EW') 
        self.lbx_console2.grid(row=9, column=2, columnspan=2, sticky='EW') 

        # trim/adjust the std mode stuff
        self.lbfm1.grid(row=3, column=0, columnspan=2, sticky='EW') 
        self.lbx_dirs1.grid(row=3, column=0, columnspan=4, sticky='EW') 
        self.lbfm_console1.grid(row=8, column= 0, columnspan=2, sticky='EW') 
        self.lbx_console1.grid(row=9, column=0, columnspan=2, sticky='EW') 




    def bindUI(self):               
        """Binds any mouse functions to the widgets in this section"""

        self.e_add1.bind('<Return>', lambda e: self.onEnter(e)) 
        self.lbx_console1.bind('<1>', lambda e: self.onLeftClick(e))
        self.lbx_console1.bind('<ButtonRelease-1>', lambda e: self.onLeftRelease(e))


        if (self.tk.call('tk', 'windowingsystem')=='aqua'):
            self.lbx_console1.bind('<2>', lambda e: self.onRightClick(e))
            # self.lbx_console1.bind('<Control-1>', lambda e: self.onRightClick(e))
            self.lbx_dirs1.bind('<2>', lambda e: self.onRightClickDirs1(e))
        else:
            self.lbx_console1.bind('<3>', lambda e: self.onRightClick(e))
            self.lbx_dirs1.bind('<3>', lambda e: self.onRightClickDirs1(e))



    # -------------------------- Widget Bindings  -------------------------- 
    # Simple actions/acknowledgement or other calls 
    # -------------------------------------------------------------------- 
    def onEnter(self, event):
        self.add1()

    def onLeftRelease(self, event):
        self.updateStatus() 

    def onLeftClick(self, event):
        self.updateStatus() 

    def onRightClick(self, event):
        self.m_console1.post(event.x_root, event.y_root)

    def onRightClickDirs1(self, event):
        self.m_dirs1.post(event.x_root, event.y_root)


    # -------------------------- Widget Actions  -------------------------- 
    # Commands & Operations 
    # -------------------------------------------------------------------- 

    def mprint(self, pstr, nl=1):
        """Prints a string pstr to messsage console, a Text widget""" 

        # This enable/disable stuff is clumsy but not too bad for a few calls
        self.t_msg.configure(state=Tk.NORMAL)
        if nl==1 or nl=='endl' or nl=='\n':
            pstr = pstr + '\n'
        self.t_msg.insert(END, pstr)
        self.t_msg.see(END)
        self.t_msg.configure(state=Tk.DISABLED)


    def updateStatus(self):
        idx_list = [int(i) for i in self.lbx_console1.curselection()]
        self.files_selected = []  # contains selection list

        total_size = 0
        for i in idx_list:
            if self.srch_log_list[i].strip()[0:2] == "##":
                continue
            else: 
                self.files_selected.append( self.srch_log_list[i].strip() )
                total_size += self.srch_sizes_list[i]

        num_files = len(self.files_selected) 
        if num_files > 0: 
            total_size = Dup.format_size(total_size)
            self.l_status.configure(text=str(num_files) + ' files selected totalling ' + total_size) 
        else:
            self.l_status.configure(text='')


 
    def openFile (self):
        """Opens selected file from console listbox"""
        # print "hello OPENFILE !!!" 
        if len(self.files_selected) == 1:
            try:
                fname = self.files_selected.pop(0)
                os.system('open ' + fname) # self.files_selected.pop(0))
            except:
                self.mprint ("Could not open file %s for some reason!" % (fname))
        elif len(self.files_selected) > 1:
            self.mprint("Cannot open multiple files. Please select ONLY one")


    def openFolder (self):
        """Opens enclosing folder of selected file in console listbox"""
        # print "hello OPENFOLDER !!!" 
        if len(self.files_selected) == 1:
            dname = os.path.dirname(self.files_selected.pop(0))
            try:
                os.system('open ' + dname) 
            except:
                self.mprint ("Could not open file %s for some reason!" % (fname))
        elif len(self.files_selected) > 1:
            self.mprint("Cannot open multiple enclosing folders. Please select ONLY one")


    def deleteFile (self):
        """Deletes selected files in console listbox"""
        # print "hello DELETE selected files"
        # Confirm deletion stuff
        files_selected_str = "Do you want to delete the selected files?\n"

        tmp_copy=self.files_selected[:]  # 20 values
        if len(tmp_copy) > 21:
            print "too many files"
            tmp_copy=self.files_selected[0:21]  # 20 values
            tmp_copy[14] = '...'
            tmp_copy[15:19] = self.files_selected[-5:-1] # 4 values
            tmp_copy[19] = self.files_selected[-1]       # last value

        files_selected_str = files_selected_str + '\n'.join(tmp_copy)
        confirm = askyesno("Confirm Deletion",  files_selected_str) 
        if not confirm:
            return

        idx_list = [int(i) for i in self.lbx_console1.curselection()]

        print "Deleting "
        for i in idx_list:
            print "-> ", self.srch_log_list[i] 
            self.lbx_console1.delete(i)
            self.lbx_console1.insert(i,"##")
            self.srch_log_list[i] = "##"

        for f in self.files_selected:
            try:
                os.unlink(f)
            except:
                self.mprint ("Could not delete file %s for some reason!" % (f))
        self.files_selected = []
        self.l_status.configure(text='Clear console and hit Search again')


    def ignoreDir (self):
        """Ignores selected file from directory listbox"""
        print "hello IGNORE !!!" 
        idx = [int(i) for i in self.lbx_dirs1.curselection()][0]
       
        dname = self.dirlist[idx] 
        if dname not in self.ignorelist:
            self.ignorelist.append(dname)
            print "self.ignorelist = ", self.ignorelist 

        self.lbx_dirs1.delete(idx)
        self.lbx_dirs1.insert(idx, dname + ' [I]') 



    def search(self):
        """Function that invokes the routine for duplicate file finding"""

        lprint = self.lbx_console1.insert  # alias

        # self.t_msg.configure(state=Tk.NORMAL)
        self.mprint("** 1. Creating file/directory structure **")
        dup_files = Dup.DuplicateFinder() 

        for p in self.ignorelist:
           print "p => ", p
           if os.path.exists(p):
               self.mprint("   Ignoring everthing under: " + os.path.abspath(p))
               dup_files.add2ignore(os.path.abspath(p))

        # go by what is in dirlist NOT what is displayed
        for p in self.dirlist:
           dup_files.update(p) 
           self.mprint("   Building structure for: " + p) 


        self.mprint("-- Directory structure creation complete --\n")
        self.mprint("** 2. Finding duplicates **\n")
   
        dup_table = dup_files.get_duplicates()
        
        self.srch_log_list, self.srch_sizes_list =  dup_files.dump_duplicates_list()

        for t in self.srch_log_list:
            lprint(END, t)


        if self.comp_modevar.get() == FIND_MODE:
            self.mprint("-- Duplicate listing complete --")

        # self.t_msg.configure(state=Tk.DISABLED)
        return

        # WHY Again??
        #tmp = self.comp_log.get() + 'Comparing stuff'
        #self.comp_log.set(tmp) 




    def clearDir(self):
        """Clears all directory lists"""
        self.dirlist = []
        self.ignorelist = []
        self.complist = []

        self.lbx_dirs1.delete(0, END)


    def clearLog(self):
        """Clears the log and consoles in the window"""

        self.srch_log_list = [] 
        self.srch_sizes_list = [] 
        self.lbx_console1.delete(0, END)
        self.t_msg.delete(1.0, END)


    def add1(self):
        """Adds directory entry into list of search dirs""" 
        # fname = askopenfilename(filetypes=[("allfiles","*"),("pythonfiles","*.py")]) #TODO
        dpath = self.e_add1.get().strip('\n').strip()
        self.e_add1.select_range(0, END)

        if dpath == '': 
            return

        if dpath in self.dirlist:
            self.mprint("Warning. Dir already added to list. %s will not be added" % (dpath))
        elif os.path.exists(dpath):
            self.dirlist.append(dpath)
            self.lbx_dirs1.insert(END, dpath)
        else:
            self.mprint("Warning. Dir path does not exist. %s will not be added" % (dpath))



    def seldir1(self):
        """Selects dir from ask open folder dialog box""" 
        dname = askdirectory(initialdir='.', title='Select Folder to Add to Search List') 
        if dname in self.dirlist:
            self.mprint("Warning. Dir already added to list. %s will not be added" % (dname))
            return
        self.dirlist.append(dname)
        self.lbx_dirs1.insert(END, dname) 
        # also populate entry box with same
        self.e_add1.delete(0, END)
        self.e_add1.insert(0, dname) 
        self.e_add1.select_range(0, END)    # also populate entry box with same



    # TODO. ---------------------------------------------------------------------------
    # TODO. Unused right now...
    # TODO. ---------------------------------------------------------------------------
    def compare(self):
        """Function that invokes the routine for comparing directories for duplicates""" 

        wprint(self.srch_log, "** 1. Creating file/directory structure **")
        dup_files = Dup.DuplicateFinder() 

        for p in self.dirlist:
           dup_files.update(p) 
           wprint(self.srch_log, "   Building structure for: " + p) 

        wprint(self.srch_log,  "-- Directory structure creation complete --\n")
        wprint(self.srch_log,  "** 2. Finding duplicates **\n")
   
        dup_table = dup_files.get_duplicates()

        tmp_list, tmp_sizes = dup_files.dump_duplicates_list() 
        wprint(self.srch_log, '\n'.join(tmp_list))

        if self.comp_modevar.get() == FIND_MODE:
            return
        tmp = self.comp_log.get() + 'Comparing stuff'
        self.comp_log.set(tmp) 


    def add2(self):
        """Adds directory entry into list of compare dirs""" 
        # Moot with display -- could comment out
        dpath = self.e_add2.get().strip('\n').strip()
        self.e_add2.select_range(0, END)

        if dpath == '': 
            return
        #if self.comp_modevar.get() == FIND_MODE:      # not in compare mode, so don't bother
        #    return              
        # fname = askopenfilename(filetypes=[("allfiles","*"),("pythonfiles","*.py")]) #TODO
        if dpath in self.complist:
            self.mprint("Warning. Dir already added to list. %s will not be added" % (dpath))
        elif os.path.exists(dpath):
            self.complist.append(self.e_add2.get())
        else:
            self.mprint("Warning. Dir path does not exist. %s will not be added" % (dpath))


    def seldir2(self):
        """Selects dir from ask open folder dialog box""" 
        dname = askdirectory(initialdir='.', title='Select Folder to Add to Compare')
        if dname in self.complist:
            self.mprint("Warning. Dir already added to list. %s will not be added" % (dname))
            return
        self.complist.append(dname)



#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Other standard functions 
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

# TODO. This is meant for temp help
def pane_example():
    """Just an example of window panes"""
    m = PanedWindow(orient=VERTICAL)
    m.pack(fill=BOTH, expand=1)
    top = Label(m, text="top pane")
    m.add(top)
    bottom = Label(m, text="bottom pane")
    m.add(bottom)
    mainloop()


def main():
    """Calls main GUI app routine"""
    app = MyApp()   # root = Tk.Tk() - implied
    app.title ("Duplicate File Finder") 
    app.mainloop()




if __name__ == "__main__":
    #from Tkinter import *
    #pane_example() 
    main()


