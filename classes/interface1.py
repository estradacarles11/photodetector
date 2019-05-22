"""
Created on Fri Sep 30 11:18:37 2016

@author: Carles Estrada
"""

import sys, os, glob, serial
import Tkinter as Tk
import tkFileDialog
from win32com.shell import shell, shellcon
import classes.photodetector as photodetector
import classes.guiwidget as guiwidget
import classes.ports as ports


class Interface():
    def __init__(self):
        
       self.ph = photodetector.photodetector()
       self.n = 0
       self.os = 0
                       
    def main(self):
        self.root = Tk.Tk()
        self.root.iconbitmap('rgb.ico')
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
              
                self.widgets.append(guiwidget.GUIWidget(self.canvas, exp1))
                if exp % 2 == 0:
                    self.widgets[exp].expframegrid(exp1, 1)
                else:
                    self.widgets[exp].expframegrid(exp, 3)
                                
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
            blaunch = Tk.Button(self.bottomframe, text = "Launch", command = self.launch)
            blaunch.grid(row = 0, column = 3)
            bsavelaunch = Tk.Button(self.bottomframe, text = "Save and launch", command = self.savelaunch)
            bsavelaunch.grid(row = 0, column = 4)
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
        
        self.newe = Tk.Tk()
        self.newe.iconbitmap('rgb.ico')
        self.newe.title("New experiment")
        
        neweframe = Tk.Frame(self.newe)
        neweframe.grid(row = 0, column = 0)
        newebottomframe = Tk.Frame(self.newe)
        newebottomframe.grid(row = 1, column = 0)
        lserport = Tk.Label(neweframe, text = "Serial Port:")
        lserport.grid(row = 0, column = 0)
        
        self.serialports()
        self.onports = []
        self.onportswid = []
        self.onportsvar = []
        self.portcount = 0
        for port in self.activeports:
            portwid = ports.Ports(neweframe, port, self.portcount)
            self.onportswid.append(portwid)
            self.portcount += 1
                         
        lnexp = Tk.Label(neweframe, text = "Number of experiments:")
        lnexp.grid(row = 0, column = 2)       
        self.enexp = Tk.Entry(neweframe)
        self.enexp.grid(row = 1, column = 2)
        
        lmes = Tk.Label(neweframe, text = "Number of measurements for each exp.:")
        lmes.grid(row = 0, column = 3)       
        self.emes = Tk.Entry(neweframe)
        self.emes.grid(row = 1, column = 3)
        
        bsavenewe = Tk.Button(newebottomframe, text = "Save", command = self.savenewe)
        bsavenewe.grid(row = 1, column = 0)
        self.newe.bind('<Return>', self.savenewe)
        self.newe.mainloop()
        
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
            self.m = int(self.emes.get())
        except:
            self.n = 0
            self.m = 0
        for i in range(self.portcount):
            var = int(self.onportswid[i].check())
            print var
            if var == 1:
                self.onports.append(self.onportswid[i].port)
        print self.onports
        self.widgets = []
        self.newe.destroy()
        self.root.destroy()
        self.main()
        
    def setparameters(self):
        self.parameters = []
        for exp in range(self.n):
            self.parameters.append([])
            self.parameters[exp] = [-1, -1, -1, -1]
            self.parameters[exp][0] = self.widgets[exp].color.get()
            self.parameters[exp][1] = self.widgets[exp].amplitude.get()
            self.parameters[exp][2] = self.widgets[exp].offset.get()
            self.parameters[exp][3] = self.widgets[exp].gain.get()
        print self.parameters
        
    def saveroot(self, event = None):
        self.setparameters()
        if self.os == 1:
            docdir =  shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0)
        elif self.os == 2:
            docdir = os.getenv("HOME")
        else:
            raise EnvironmentError('Unsupported platform')
        self.initdir = "%s\\Photodetector\\Experiment Files" % docdir
        self.filename = tkFileDialog.asksaveasfilename(initialdir = self.initdir, title = "Save exp. file as...", filetypes = (("Text file", ".txt"),("all files", "*.*")))
        try:
            self.file = open(self.filename, 'w')
            print "File %s created!" % self.filename
            
            self.file.write("Active serial ports:\n")
            self.file.write("%s" % self.onports)
            self.file.write("\nNumber of experiments:\n%s\nNumber of measurements for each experiment:\n%s\n" % (self.n, self.m))
            for exp in range(self.n):
                exp1 = exp + 1
                self.file.write("Experiment %s:\n" % exp1)
                self.file.write("%s\n" % self.parameters[exp])
            self.file.close()
        except:
            print "Error while saving file."
    
    def launch(self, event = None):
        self.newp = [2, 0.023, 0.85, 2]
        self.setparameters()
        
        if self.os == 1:
            docdir =  shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0)
        elif self.os == 2:
            docdir = os.getenv("HOME")
        else:
            raise EnvironmentError('Unsupported platform')
        self.initdir = "%s\\Photodetector\\Output" % docdir
        self.filename = tkFileDialog.asksaveasfilename(initialdir = self.initdir, title = "Save output as...", filetypes = (("Text file", ".txt"),("all files", "*.*")))
        
        for port in self.onports:
            self.ph.connectarduino(port)
            for i in self.parameters:
                self.oldp = self.newp
                self.newp = i
                self.ph.sendparameters(self.oldp, self.newp)
                self.ph.record(self.n + 2)
        
        try:
            self.file = open(self.filename, 'w')
            for i in self.ph.output:
                self.file.write("%s\n" % i)
                self.file.close()
        except:
            print "Error while saving file."
            
    def savelaunch(self, event = None):
        self.saveroot()
        self.launch()
        
    def openexpfile(self):
        if self.os == 1:
            docdir =  shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0)
        elif self.os == 2:
            docdir = os.getenv("HOME")
        else:
            raise EnvironmentError('Unsupported platform')
        self.initdir = "%s\\Photodetector\\Experiment Files" % docdir
        self.filename = tkFileDialog.askopenfilename(initialdir = self.initdir, title = "Open exp. file", filetypes = (("Text file", ".txt"),("all files", "*.*")))
        #try:
        self.file = open(self.filename, 'r')
        self.output = self.file.readlines()
        self.onports = self.output[1]
        self.n = int(self.output[3])
        self.m = int(self.output[5])
        self.parameters = []
        self.widgets = []
        self.root.destroy()
        self.main()
        
        for exp in range(self.n):
            line = 2 * exp + 7
            llist = self.output[line].split()
            lllist = []
            count = 0
            for i in llist:
                if count >= 1:
                    i = float(i[:-1])
                else:
                    i = int(i[1:-1])
                lllist.append(i)
                count += 1
            self.parameters.append(lllist)
            
            self.widgets[exp].setcolor(self.parameters[exp][0])
            self.widgets[exp].setamplitude(self.parameters[exp][1])
            self.widgets[exp].setoffset(self.parameters[exp][2])
            self.widgets[exp].setgain(self.parameters[exp][3])
        

        #except:
            #print "Error while opening file."
    
    def analizeresults(self):
        pass
    
    def about(self):
        pass