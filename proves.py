"""
Created on Fri Sep 30 11:18:37 2016

@author: Carles Estrada
"""

import Tkinter as Tk

class Ports():
    def __init__(self, frame, port, row):
        self.frame = frame
        self.port = port
        self.row = row
        self.var = Tk.BooleanVar()
        
        self.widget(self.var, self.row)
        
    def check(self):
        i = self.var.get()
        if i:
            print self.port
            return int(1)
        elif not i: 
            print i
            return int(0)
        else:
            print "Error"
            
    def widget(self, var, row):
        cb = Tk.Checkbutton(self.frame, text = self.port, variable = var, command = self.check)
        cb.grid(row = row, column = 1)
        
        
import serial
        
class Interface():
    def __init__(self):
        pass
        
    def main(self):
        def newexperiment():
            self.activeports =  []
            self.onports = []
            self.newe = Tk.Tk()
            
            neweframe = Tk.Frame(self.newe)
            neweframe.grid(row = 0, column = 0)
            newebottomframe = Tk.Frame(self.newe)
            newebottomframe.grid(row = 1, column = 0)
            lserport = Tk.Label(neweframe, text = "Serial Port:")
            lserport.grid(row = 0, column = 0)
            
            self.serialports()
            self.onports = []
            self.onportswid = []
            self.portcount = 0
            for port in self.activeports:
                self.onportswid.append(Ports(neweframe, port, self.portcount))
                self.portcount += 1
                                     
            bsavenewe = Tk.Button(newebottomframe, text = "Save", command = self.savenewe)
            bsavenewe.grid(row = 1, column = 0)
            self.newe.bind('<Return>', self.savenewe)
            self.newe.mainloop()
        self.root = Tk.Tk()        
        newexp = Tk.Button(self.root, text = "New experiment", command = newexperiment)
        newexp.grid(row = 0, column = 1, sticky = Tk.E + Tk.W)
        self.root.mainloop()
                
        
        
    def serialports(self):
        self.ports = ['COM%s' % (i + 1) for i in range(256)]
        
        for port in self.ports:
            try:
                s = serial.Serial(port)
                s.close()
                self.activeports.append(port)
            except (OSError, serial.SerialException):
                pass
   
    def savenewe(self, event = None):
        for i in range(self.portcount):
            var = int(self.onportswid[i].check())
            print var
            if var == 1:
                self.onports.append(self.onportswid[i].port)
        print self.onports
        self.newe.destroy()
        self.root.destroy()
        self.main()

gui = Interface()

gui.main()

#gui.main()

