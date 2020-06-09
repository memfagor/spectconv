#!/usr/bin/env python3

import os
import tkinter as Tk
from tkinter import filedialog as Fd
#import fileslist as Fl

class Model:
    def __init__(self):
        self.filelist = []

    def getfiles(self, path, extension):
        self.filelist = Fd.askopenfiles(initialdir=path, mode='r',
                filetypes=[(extension, '*.'+extension)])

class View:
    def __init__(self, master, model):
        self.frame = Tk.Frame(master)
        self.model = model
        self.frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.mainpanel = MainPanel(master)
        self.sidepanel = SidePanel(master)
        self.sidepanel.fillButton.bind("<Button>", self.fill)
        self.sidepanel.clearButton.bind("<Button>", self.clear)

    def fill(self, event):
        self.model.getfiles(os.getcwd(),'csv')
        for item in self.model.filelist:
            self.mainpanel.listbox.insert(Tk.END, item.name)

    def clear(self, event):
        self.mainpanel.listbox.delete(0, Tk.END)


class MainPanel:
    def __init__(self, root):
        self.listbox = Tk.Listbox(root, selectmode=Tk.EXTENDED)
        self.listbox.pack(fill=Tk.BOTH, expand=1)

class SidePanel():
    def __init__(self, root):
        self.frame = Tk.Frame(root)
        self.frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.fillButton = Tk.Button(self.frame, text="Fill")
        self.fillButton.pack(side="top", fill=Tk.BOTH)
        self.clearButton = Tk.Button(self.frame, text="Clear")
        self.clearButton.pack(side="top", fill=Tk.BOTH)

class Controller:
    def __init__(self):
        self.root = Tk.Tk()
        self.model = Model()
        self.view = View(self.root, self.model)

    def run(self):
        self.root.title("Spectconv")
        self.root.deiconify()
        self.root.mainloop()

if __name__ == '__main__':
    c = Controller()
    c.run()
