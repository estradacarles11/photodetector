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
            self.canvas.grid(row = 0, column = 0, sticky = Tk.N + Tk.S + Tk.E + Tk.W)
            
            self.bottomframe = Tk.Frame(self.root)
            self.bottomframe.grid(row = 1, column = 0)
        
            for exp in range(self.n):
                #self.setcaog.append([])
                self.widgets.append([[], [], [], []])
                self.parameters.append([-1, -1, -1, -1])
                self.var.append([-1, -1, -1, -1])
                self.min.append([self.minamp, self.minoff, self.minga])
                self.max.append([self.maxamp, self.maxoff, self.maxga])
                self.var[exp][0] = Tk.IntVar()
                self.var[exp][1] = Tk.IntVar()
                self.var[exp][2] = Tk.IntVar()
                self.var[exp][3] = Tk.IntVar()
                exp1 = exp + 1
                
                lxempt0 = Tk.Label(self.canvas, text = "       ")
                lxempt0.grid(row = exp, column = 0)
                lxempt2 = Tk.Label(self.canvas, text = "       ")
                lxempt2.grid(row = exp, column = 2)
                lxempt4 = Tk.Label(self.canvas, text = "       ")
                lxempt4.grid(row = exp, column = 4)
                lyempt1 = Tk.Label(self.canvas, text = "")
                lyempt1.grid(row = 0, column = 0, sticky = "W")
                lyempt2 = Tk.Label(self.canvas, text = "")
                lyempt2.grid(row = exp + 2, column = 0, sticky = "W")
                                    
                self.lexp = Tk.LabelFrame(self.canvas, text = "Experiment %s:" % exp1)
                self.lexp.grid(sticky = "W")    
                
                if exp % 2 == 0:
                    self.lexp.grid(row = exp + 1, column = 1)
                else:
                    self.lexp.grid(row = exp, column = 3)
                
                
                #Color
                #self.setcaog[exp].append(self.setcolor(exp))                    
                self.widgets[exp][0].append(Tk.Label(self.lexp, text = "Color:"))
                self.widgets[exp][0][0].grid(row = 1, column = 0, sticky = "W")
                self.widgets[exp][0].append(Tk.Radiobutton(self.lexp, text= "Red", variable = self.var[exp][0], value = 2, command = lambda: self.setcolor(exp)))
                self.widgets[exp][0][1].grid(row = 1, column = 1, sticky = "W")
                self.widgets[exp][0].append(Tk.Radiobutton(self.lexp, text= "Green", variable = self.var[exp][0], value = 1, command = lambda: self.setcolor(exp)))
                self.widgets[exp][0][2].grid(row = 1, column = 2, sticky = "W")
                self.widgets[exp][0].append(Tk.Radiobutton(self.lexp, text= "Blue", variable = self.var[exp][0], value = 0, command = lambda: self.setcolor(exp)))
                self.widgets[exp][0][3].grid(row = 1, column = 3, sticky = "W")
                
                
                #Amplitude
                self.widgets[exp][1].append(Tk.Label(self.lexp, text = "Amplitude:"))
                self.widgets[exp][1][0].grid(row = 2, column = 0, sticky = "W")
                self.widgets[exp][1].append(Tk.Scale(self.lexp, variable = self.var[exp][1], from_ = self.min[exp][0], to = self.max[exp][0], orient = Tk.HORIZONTAL, resolution = 0.05, length = 150))
                self.widgets[exp][1][1].grid(row = 2, column = 1, sticky = "W", columnspan = 3)
                self.widgets[exp][1].append(Tk.Entry(self.lexp))
                self.widgets[exp][1][2].grid(row = 2, column = 4, sticky = "W")
                
                #Offset                
                self.widgets[exp][2].append(Tk.Label(self.lexp, text = "Offset:"))
                self.widgets[exp][2][0].grid(row = 3, column = 0, sticky = "W")
                self.widgets[exp][2].append(Tk.Scale(self.lexp, variable = self.var[exp][2], from_ = self.min[exp][1], to = self.max[exp][1], orient = Tk.HORIZONTAL, resolution = 0.05, length = 150))
                self.widgets[exp][2][1].grid(row = 3, column = 1, sticky = "W", columnspan = 4)
                self.widgets[exp][2].append(Tk.Entry(self.lexp))
                self.widgets[exp][2][2].grid(row = 3, column = 4, sticky = "W")
                
                #Gain                
                self.widgets[exp][3].append(Tk.Label(self.lexp, text = "Gain:"))
                self.widgets[exp][3][0].grid(row = 4, column = 0, sticky = "W")
                self.widgets[exp][3].append(Tk.Scale(self.lexp, variable = self.var[exp][3], from_ = self.min[exp][2], to = self.max[exp][2], orient = Tk.HORIZONTAL, resolution = 0.05, length = 150))
                self.widgets[exp][3][1].grid(row = 4, column = 1, sticky = "W", columnspan = 4)
                self.widgets[exp][3].append(Tk.Entry(self.lexp))
                self.widgets[exp][3][2].grid(row = 4, column = 4, sticky = "W")
                
                
                
            if self.n > 8:
                yscrollbar = Tk.Scrollbar(self.mainframe)
                yscrollbar.grid(row = 0, column = 1, sticky = Tk.N + Tk.S)
                self.canvas.config(yscrollcommand = yscrollbar.set, scrollregion = (0, 0, 500, 500))
                yscrollbar.config(command = self.canvas.yview)
                    
            breset = Tk.Button(self.bottomframe, text = "Reset", command = self.newexperiment)
            breset.grid(row = 0, column = 1)
            bsave = Tk.Button(self.bottomframe, text = "Save", command = self.saveroot)
            bsave.grid(row = 0, column = 2)
            bsavelaunch = Tk.Button(self.bottomframe, text = "Save and launch", command = self.savelaunch)
            bsavelaunch.grid(row = 0, column = 3)
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
        print self.onportsvar
        for port in self.activeports:
            var = int(self.onportsvar[self.activeports.index(port)].get())
            if var == 1:
                self.onports.append(port)
        print self.onports
        print self.n
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