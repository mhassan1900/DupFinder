#!c:\apps\python27\python.exe

import Tkinter as Tk

class MainApp(Tk.Tk):
    def __init__(self,parent):
        Tk.Tk.__init__(self,parent)
        # keep reference in case we need parent
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entryVariable = Tk.StringVar()

        # why do we need to pass our own objects? 
        # self.entry = Tk.Entry(self)
        self.entry = Tk.Entry(textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter text here.")

        # no need to keep internal state of button in this case
        # button = Tk.Button(self,text=u"Click me !")
        button = Tk.Button(text=u"Click me !",
                                command=self.OnButtonClick)
        button.grid(column=1,row=0)

        self.labelVariable = Tk.StringVar()

        #label = Tk.Label(self,
        #                      anchor="w",fg="white",bg="blue")
        label = Tk.Label(anchor="w",fg="white",bg="blue",
        self.labelVariable = Tk.StringVar()
        label = Tk.Label(self,textvariable=self.labelVariable,
                            textvariable=self.labelVariable)
        label.grid(column=0,row=1,columnspan=2,sticky='EW')

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
   
    def OnButtonClick(self):
        self.labelVariable.set("You clicked the button !")
      

    def OnPressEnter(self,event):
        self.labelVariable.set("You pressed enter !")


if __name__ == "__main__":
    root = MainApp(None)
    root.title("Main App")
    root.mainloop()

