"""
Created on Fri Sep 30 11:18:37 2016

@author: Carles Estrada
"""

import Tkinter as Tk

class Ports():
    def __init__(self, frame, port, row, instance):
        self.frame = frame
        self.port = port
        self.row = row
        self.instance = instance
        self.var = Tk.BooleanVar()
                
        self.widget(self.var, self.row)
        
    def check(self):
        i = self.var.get()
        self.instance.portcheck(self.port, i)
        return i
                
    def setport(self, tf):
        if tf == 0:
            self.cb.deselect()
        else:
            self.cb.select()
        
        self.check()
            
    def widget(self, var, row):
        self.cb = Tk.Checkbutton(self.frame, text = self.port, variable = var, command = self.click)
        self.cb.grid(row = row, column = 1)
        
    def click(self):
        self.check()
        if self.instance.t:
            self.instance.widgets[0].getports(self.instance)