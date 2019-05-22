# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 16:06:19 2016

@author: Carles Estrada
"""

import sys, os, glob, serial
import Tkinter as Tk
import tkFileDialog
from win32com.shell import shell, shellcon
import classes.photodetector as photodetector

class PhWidget():
    def __init__(self, main, experiment):
        self.main = main
        self.exp = experiment
        self.minamp = 0.023
        self.minoff = 0.85
        self.minga = 0.85
        self.maxamp = 1.1
        self.maxoff = 2.046
        self.maxga = 2.046
        
        self.expframe()
    
    def expframe(self):
        self.lexp = Tk.LabelFrame(self.main, text = "Experiment %s:" % self.exp)
        self.setcolor(1)
        self.setamplitude(2)
        self.setoffset(3)
        self.setgain(4)
    
    def setcolor(self, nrow):
        self.color = Tk.IntVar()
        lcolor = Tk.Label(self.lexp, text = "Color:")
        lcolor.grid(row = nrow, column = 0, sticky = "W")
        rred = Tk.Radiobutton(self.lexp, text= "Red", variable = self.color, value = 2, command = self.getcolor)
        rred.grid(row = nrow, column = 1, sticky = "W")
        rgreen = Tk.Radiobutton(self.lexp, text= "Green", variable = self.color, value = 1, command = self.getcolor)
        rgreen.grid(row = nrow, column = 2, sticky = "W")
        rblue = Tk.Radiobutton(self.lexp, text= "Blue", variable = self.color, value = 0, command = self.getcolor)
        rblue.grid(row = nrow, column = 3, sticky = "W")
    
    def setamplitude(self, nrow):
        self.amplitude = Tk.DoubleVar()
        lamp = Tk.Label(self.lexp, text = "Amplitude:")
        lamp.grid(row = nrow, column = 0, sticky = "W")
        self.samp = Tk.Scale(self.lexp, variable = self.amplitude, from_ = self.minamp, to = self.maxamp, showvalue = 0, orient = Tk.HORIZONTAL, resolution = 0.001, length = 150, command = self.getamplitude)
        self.samp.grid(row = nrow, column = 1, sticky = "W", columnspan = 3)
        self.eamp = Tk.Entry(self.lexp, width = 6)
        self.eamp.grid(row = nrow, column = 4, sticky = "W")
        checkbutton = Tk.Button(self.lexp, text = "Check", command = self.geteamp)
        checkbutton.grid(row = nrow, column = 5, sticky = Tk.E + Tk.W)
        
    def setoffset(self, nrow):
        self.offset = Tk.DoubleVar()
        loff = Tk.Label(self.lexp, text = "Offset:")
        loff.grid(row = nrow, column = 0, sticky = "W")
        self.soff = Tk.Scale(self.lexp, variable = self.offset, from_ = self.minoff, to = self.maxoff, showvalue = 0, orient = Tk.HORIZONTAL, resolution = 0.001, length = 150, command = self.getoffset)
        self.soff.grid(row = nrow, column = 1, sticky = "W", columnspan = 3)
        self.eoff = Tk.Entry(self.lexp, width = 6)
        self.eoff.grid(row = nrow, column = 4, sticky = "W")
        checkbutton = Tk.Button(self.lexp, text = "Check", command = self.geteoff)
        checkbutton.grid(row = nrow, column = 5, sticky = Tk.E + Tk.W)
    
    def setgain(self, nrow):
        self.gain = Tk.DoubleVar()
        lga = Tk.Label(self.lexp, text = "Gain:")
        lga.grid(row = nrow, column = 0, sticky = "W")
        self.sga = Tk.Scale(self.lexp, variable = self.gain, from_ = self.minga, to = self.maxga, showvalue = 0, orient = Tk.HORIZONTAL, resolution = 0.001, length = 150, command = self.getgain)
        self.sga.grid(row = nrow, column = 1, sticky = "W", columnspan = 3)
        self.ega = Tk.Entry(self.lexp, width = 6)
        self.ega.grid(row = nrow, column = 4, sticky = "W")
        checkbutton = Tk.Button(self.lexp, text = "Check", command = self.getega)
        checkbutton.grid(row = nrow, column = 5, sticky = Tk.E + Tk.W)
    
    def getcolor(self):
        col = self.color.get()
        if col == 0:
            self.maxamp = 1.1
            self.maxoff = 2.046
            self.maxga = 2.046
        elif col == 1:
            self.maxamp = 0.242
            self.maxoff = 1.958
            self.maxga = 2.046
        elif col == 2:
            self.maxamp = 1.1
            self.maxoff = 2.046
            self.maxga = 2.046

        self.samp.config(from_ = self.minamp, to = self.maxamp)
        self.soff.config(from_ = self.minoff, to = self.maxoff)
        self.sga.config(from_ = self.minga, to = self.maxga)
        return col
        
    def getamplitude(self, a):
        amp = float(a)
        if self.maxoff + amp > 2.75:
            maxoffset = 2.75 - amp
            if maxoffset < self.maxoff:
                self.maxoff = maxoffset
                self.soff.config(to = self.maxoff)
        self.eamp.delete(0, Tk.END)
        self.eamp.insert(0, amp)
        return amp
    
    def geteamp(self):
        amp = float(self.eamp.get())
        if amp > self.maxamp or amp < self.minamp:
            self.eamp.delete(0, Tk.END)
        else:
            self.samp.set(amp)
            self.getamplitude()
        
    def getoffset(self, o):
        off = float(o)
        if self.maxamp + off > 2.75:
            maxamplitude = 2.75 - off
            if maxamplitude < self.maxamp:
                self.maxamp = maxamplitude
                self.samp.config(to = self.maxamp)
        self.eoff.delete(0, Tk.END)
        self.eoff.insert(0, off)
        return off
    
    def geteoff(self):
        off = float(self.eoff.get())
        if off > self.maxoff or off < self.minoff:
            self.eoff.delete(0, Tk.END)
        else:
            self.soff.set(off)
            self.getoffset()         
            
    def getgain(self, g):
        ga = float(g)
        self.ega.delete(0, Tk.END)
        self.ega.insert(0, ga)
        return ga
    
    def getega(self):
        ga = float(self.ega.get())
        if ga > self.maxga or ga < self.minga:
            self.ega.delete(0, Tk.END)
        else:
            self.sga.set(ga)
            self.getgain()
        
    def expframegrid(self, row, column):
        self.lexp.grid(row = row, column = column, sticky = "W")


class Interface():
    def __init__(self):
        
       self.ph = photodetector.photodetector()
       self.n = 0
       self.os = 0
                       
    def main(self):
        self.root = Tk.Tk()
        self.root.iconbitmap('transparent.ico')
        self.root.title("Photodetector")
        self.root.resizable(0, 0)
        
        #self.mainframe = Tk.Frame(self.root)
        #self.mainframe.columnconfigure(0, weight=1)
        #self.mainframe.rowconfigure(0, weight=1)
        
        menubar = Tk.Menu(self.root)
        
        filemenu = Tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "File", menu = filemenu)
        filemenu.add_command(label = "New experiment", command = self.newexperiment)
        filemenu.add_command(label = "Open exp. file", command = self.openexpfile)
        filemenu.add_separator()
        filemenu.add_command(label = "Save results", command = self.saveresults)
        filemenu.add_command(label = "Save results as...", command = self.saveresultsas)
        filemenu.add_separator()
        filemenu.add_command(label = "Exit", command = self.root.destroy)
        
        resultsmenu = Tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "Results", menu = resultsmenu)
        resultsmenu.add_command(label = "Analyze results", command = self.analizeresults)
        
        helpmenu = Tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "Help", menu = helpmenu)
        helpmenu.add_command(label = "About...", command = self.about)
        
        self.root.config(menu = menubar)
        
        if self.n == 0:
            lempt = Tk.Label(self.root, text = "                       ")
            lempt.grid(row = 0, column = 0)
            rempt = Tk.Label(self.root, text = "                       ")
            rempt.grid(row = 0, column = 2)
            newexp = Tk.Button(self.root, text = "New experiment", command = self.newexperiment)
            newexp.grid(row = 0, column = 1, sticky = Tk.E + Tk.W)
            openexp = Tk.Button(self.root, text = "Open exp. file", command = self.openexpfile)
            openexp.grid(row = 1, column = 1, sticky = Tk.E + Tk.W)
            exitexp = Tk.Button(self.root, text = "Exit", command = self.root.destroy)
            exitexp.grid(row = 2, column = 1, sticky = Tk.E + Tk.W)
            
        else:  
            self.mainframe = Tk.Frame(self.root)
            self.mainframe.grid(row = 0, column = 0)
            self.mainframe.grid_rowconfigure(0, weight = 1)
            self.mainframe.grid_columnconfigure(0, weight = 1)
            self.canvas = Tk.Canvas(self.mainframe, height = 500, width = 500)
            self.canvas.grid(row = 0, column = 0, sticky = Tk.N + Tk.E + Tk.S + Tk.W)
            self.bottomframe = Tk.Frame(self.root)
            self.bottomframe.grid(row = 1, column = 0)
        
            for exp in range(self.n):
                exp1 = exp + 1
                
                lxempt0 = Tk.Label(self.canvas, text = "       ")
                lxempt0.grid(row = exp, column = 0)
                if self.n > 1:
                    lxempt2 = Tk.Label(self.canvas, text = "       ")
                    lxempt2.grid(row = exp, column = 2)
                lxempt4 = Tk.Label(self.canvas, text = "       ")
                lxempt4.grid(row = exp, column = 4)
                lyempt1 = Tk.Label(self.canvas, text = "")
                lyempt1.grid(row = 0, column = 0, sticky = "W")
                lyempt2 = Tk.Label(self.canvas, text = "")
                lyempt2.grid(row = exp + 2, column = 0, sticky = "W")
              
                experiment = PhWidget(self.canvas, exp1)
                if exp % 2 == 0:
                    experiment.expframegrid(exp1, 1)
                else:
                    experiment.expframegrid(exp, 3)
                                
            if self.n > 8:
                self.root.resizable(0, 1)
                self.root.minsize(width = 250, height = 75)
                self.root.maxsize(width = 720, height = 700)
                self.mainframe.config(height = 700, width = 720)
                yscrollbar = Tk.Scrollbar(self.mainframe)
                yscrollbar.grid(row = 0, column = 1, sticky = Tk.N + Tk.S)
                self.canvas.config(scrollregion = self.canvas.bbox(Tk.ALL), yscrollcommand = yscrollbar.set)
                yscrollbar.config(command = self.canvas.yview)
                    
            breset = Tk.Button(self.bottomframe, text = "Reset", command = self.newexperiment)
            breset.grid(row = 0, column = 1)
            bsave = Tk.Button(self.bottomframe, text = "Save", command = self.saveroot)
            bsave.grid(row = 0, column = 2)
            bsavelaunch = Tk.Button(self.bottomframe, text = "Save and launch", command = self.savelaunch)
            bsavelaunch.grid(row = 0, column = 3)
            lyempt3 = Tk.Label(self.bottomframe, text = "")
            lyempt3.grid(row = 1, column = 0, sticky = "W")
            self.root.bind('<Return>', self.savelaunch)          
            
        if sys.platform.startswith('win'):
            self.os = 1
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            self.os = 2
        elif sys.platform.startswith('darwin'):
            self.os = 3
        else:
            raise EnvironmentError('Unsupported platform')
        
        self.root.mainloop()
            
    def newexperiment(self):
        
        self.activeports =  []
        self.onports = []
        self.parameters = []
        self.var = []
        self.widgets = []
        self.minamp = 0.023
        self.minoff = 0.85
        self.minga = 0.85
        self.maxamp = 1.1
        self.maxoff = 2.046
        self.maxga = 2.046
        self.min = []
        self.max = []
        #self.setcaog = []

        self.newe = Tk.Tk()
        self.newe.iconbitmap('transparent.ico')
        self.newe.title("New experiment")
        
        neweframe = Tk.Frame(self.newe)
        neweframe.grid(row = 0, column = 0)
        newebottomframe = Tk.Frame(self.newe)
        newebottomframe.grid(row = 1, column = 0)
        lserport = Tk.Label(neweframe, text = "Serial Port:")
        lserport.grid(row = 0, column = 0)
        self.serialports()
        self.onports = []
        self.onportsvar = []
        for port in self.activeports:
            self.onportsvar.append(-1)
            self.onportsvar[self.activeports.index(port)] = Tk.IntVar()
            mserport = Tk.Checkbutton(neweframe, text = port, variable = self.onportsvar[self.activeports.index(port)], onvalue = 1, offvalue = 0)
            mserport.grid(row = self.activeports.index(port), column = 1)
                
        lnexp = Tk.Label(neweframe, text = "Number of experiments:")
        lnexp.grid(row = 0, column = 2)       
        self.enexp = Tk.Entry(neweframe)
        self.enexp.grid(row = 1, column = 2)
        
        bsavenewe = Tk.Button(newebottomframe, text = "Save", command = self.savenewe)
        bsavenewe.grid(row = 1, column = 0)
        self.newe.bind('<Return>', self.savenewe)
        
    def setcolor(self, exp):
        
        color = self.var[exp][0].get()
        self.setparameters(exp, 0, color)
        print exp, color
        
        if color == 0:
            self.max[exp][0] = 1.1
            self.max[exp][1] = 2.046
            self.max[exp][2] = 2.046
        elif color == 1:
            self.max[exp][0] = 0.242
            self.max[exp][1] = 1.958
            self.max[exp][2] = 2.046
        elif color == 2:
            self.max[exp][0] = 1.1
            self.max[exp][1] = 2.046
            self.max[exp][2] = 2.046

        self.widgets[exp][1][1].config(from_ = self.min[exp][0], to = self.max[exp][0])
        self.widgets[exp][2][1].config(from_ = self.min[exp][1], to = self.max[exp][1])
        self.widgets[exp][3][1].config(from_ = self.min[exp][2], to = self.max[exp][2])
        
    
    def setamplitude(self):
        pass
    
    def setoffset(self):
        pass
    
    def setgain(self):
        pass
    
    def setparameters(self, experiment, parameter, value):
        self.parameters[experiment][parameter] = value
    

        
    def serialports(self):
        if self.os == 1:
            self.ports = ['COM%s' % (i + 1) for i in range(256)]
        elif self.os == 2:
            self.ports = glob.glob('/dev/tty[A-Za-z]*')
        elif self.os == 3:
            self.ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
    
        for port in self.ports:
            try:
                s = serial.Serial(port)
                s.close()
                self.activeports.append(port)
            except (OSError, serial.SerialException):
                pass
   
    def savenewe(self, event = None):
        try:
            self.n = int(self.enexp.get())
        except:
            self.n = 0
        for port in self.activeports:
            var = int(self.onportsvar[self.activeports.index(port)].get())
            if var == 1:
                self.onports.append(port)
        self.newe.destroy()
        self.root.destroy()
        self.main()
        
    def saveroot(self, event = None):
        for exp in range(self.n):
            for v in range(4):
                self.setparameters(exp, 0, self.var[exp][v].get())
        if self.os == 1:
            docdir =  shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0)
        elif self.os == 2:
            docdir = os.getenv("HOME")
        else:
            raise EnvironmentError('Unsupported platform')
        self.initdir = "%s\\Photodetector" % docdir
        self.filename = tkFileDialog.asksaveasfilename(initialdir = self.initdir, title = "Save exp. file as...", filetypes = (("Text file", ".txt"),("all files", "*.*")))
        try:
            self.file = open(self.filename, 'w')
            print "File %s created!" % self.filename
            
            self.file.write("Active serial ports:\n")
            for port in self.onports:
                self.file.write("%s\n" % port)
            self.file.write("\nNumber of experiments:\n%s\n\n" % self.n)
            for exp in range(self.n):
                exp1 = exp + 1
                self.file.write("Experiment %s:\n" % exp1)
            self.file.close()
        except:
            raise "Error while saving file."
    
    def savelaunch(self, event = None):
        self.saveroot()
        
    def openexpfile(self):
        pass
    
    def saveresults(self):
        pass
    
    def saveresultsas(self):
        pass
    
    def analizeresults(self):
        pass
    
    def about(self):
        pass


gui = Interface()
gui.main()