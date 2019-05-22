"""
Created on Fri Sep 30 11:18:37 2016

@author: Carles Estrada
"""

import sys, os, glob, serial
import Tkinter as Tk
import tkFileDialog
from win32com.shell import shell, shellcon
import photodetector
import guiwidget
import ports

class Interface():
    def __init__(self):
        
       self.ph = photodetector.photodetector()
       self.os = 0
                       
    def main(self):
        self.root = Tk.Tk()
        self.root.iconbitmap('rgb.ico')
        self.root.title("Photodetector")
        self.root.resizable(0, 0)
                
        self.menubar()
        
        self.n = Tk.IntVar()
        self.j = 0
        self.presamp = 5
        
        self.topframe = Tk.Frame(self.root)
        self.topframe.grid(row = 0, column = 0, sticky = Tk.W)
        lemptop0 = Tk.Label(self.topframe, text = "       ")
        lemptop0.grid(row = 0, column = 0)
        lemptop1 = Tk.Label(self.topframe, text = "       ")
        lemptop1.grid(row = 1, column = 2)
        lemptop3 = Tk.Label(self.topframe, text = "       ")
        lemptop3.grid(row = 1, column = 4)
        lemptop3 = Tk.Label(self.topframe, text = "       ")
        lemptop3.grid(row = 1, column = 6)
        
        lnexp = Tk.LabelFrame(self.topframe, text = "Number of experiments:")
        lnexp.grid(row = 0, column = 1)
        lempt = Tk.Label(lnexp, text = "   ")
        lempt.grid(row = 0, column = 0)
        rempt = Tk.Label(lnexp, text = "   ")
        rempt.grid(row = 0, column = 4)
        self.snexp = Tk.Scale(lnexp, variable = self.n, from_ = 0, to = 8, showvalue = 0, orient = Tk.HORIZONTAL, resolution = 1, command = self.getsn)
        self.snexp.grid(row = 0, column = 1)
        self.enexp = Tk.Entry(lnexp, width = 6)
        self.enexp.grid(row = 0, column = 2)
        bnexp = Tk.Button(lnexp, text = "Apply", command = self.geten)
        bnexp.grid(row = 0, column = 3)
        
        lpresamp = Tk.LabelFrame(self.topframe, text = "Samples:")
        lpresamp.grid(row = 0, column = 3)
        lempt = Tk.Label(lpresamp, text = "   ")
        lempt.grid(row = 0, column = 0)
        rempt = Tk.Label(lpresamp, text = "   ")
        rempt.grid(row = 0, column = 3)
        self.epresamp = Tk.Entry(lpresamp, width = 6)
        self.epresamp.grid(row = 0, column = 1)
        self.epresamp.insert(0, self.presamp)
        bnexp = Tk.Button(lpresamp, text = "Apply", command = self.getpresamp)
        bnexp.grid(row = 0, column = 2)
        
        lports = Tk.LabelFrame(self.topframe, text = "Serial ports:")
        lports.grid(row = 0, column =5)
        lempt = Tk.Label(lports, text = "   ")
        lempt.grid(row = 0, column = 0)
        rempt = Tk.Label(lports, text = "   ")
        rempt.grid(row = 0, column = 2)
        
        self.detectos()
        self.activeports =  []
        self.portswid = []
        self.serialports()
        
        noport = ports.Ports(lports, "None", 0)
        self.portswid.append(noport)
        portcount = 1
        
        for port in self.activeports:
            portwid = ports.Ports(lports, port, portcount)
            self.portswid.append(portwid)
            portcount += 1
        
        self.portswid[0].set(1)
                 
        self.root.mainloop()        
        
    def menubar(self):
        
        menubar = Tk.Menu(self.root)
        
        filemenu = Tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "File", menu = filemenu)
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
    
    def getsn(self, a):
        n = int(a)
        self.enexp.delete(0, Tk.END)
        self.enexp.insert(0, n)
        self.n = n
        
        self.widgetframe()
    
    def geten(self):
        n = int(self.enexp.get())
        if n > 8 or n < 0:
            self.enexp.delete(0, Tk.END)
        else:
            self.snexp.set(n)
        self.n = n
            
        self.widgetframe()
        
    def getpresamp(self):
        self.presamp = int(self.epresamp.get())
        try:
            for exp in range(self.n):
                self.widgets[exp].setsamples(self.presamp)
        except:
            pass
        
    def widgetframe(self):
        if self.n == 0:
            try:
                self.mainframe.grid_remove()
                self.bottomframe.grid_remove()
            except:
                pass            
        elif self.j == 0:
            self.widgets = []
        
            self.mainframe = Tk.Frame(self.root)
            self.mainframe.grid(row = 1, column = 0)
            self.mainframe.grid_rowconfigure(0, weight = 1)
            self.mainframe.grid_columnconfigure(0, weight = 1)
            
            self.bottomframe = Tk.Frame(self.root)
            self.bottomframe.grid(row = 2, column = 0)
        
            lxempt0 = Tk.Label(self.mainframe, text = "       ")
            lxempt0.grid(row = 0, column = 0)
            
            breset = Tk.Button(self.bottomframe, text = "Reset", command = self.reset)
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
                   
        if self.n > self.j:
            self.generatewidgets()
            
        elif self.n < self.j:
            self.deletewidgets()
            
    def generatewidgets(self):
        new = self.n - self.j
        
        for num in range(new):
            exp = self.j + num
            exp1 = exp + 1
            
            if len(self.widgets) < exp1:
                self.widgets.append(guiwidget.GUIWidget(self.mainframe, exp1, self.presamp))
            
            if exp % 2 == 0:
                self.widgets[exp].expframegrid(exp, 1)
            else:
                self.widgets[exp].expframegrid(exp - 1, 3)
                
        self.j = self.n
        
    def deletewidgets(self):        
        for exp in range(self.j):
            exp1 = exp + 1
            if exp1 > self.n:
                self.widgets[exp].forget()
                
        self.j = self.n
        
    def detectos(self):
        if sys.platform.startswith('win'):
            self.os = 1
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            self.os = 2
        elif sys.platform.startswith('darwin'):
            self.os = 3
        else:
            raise EnvironmentError('Unsupported platform')

    def serialports(self):
        if self.os == 1:
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif self.os == 2:
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif self.os == 3:
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
    
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                self.activeports.append(port)
            except:
                pass
            
    def noports(self):
        print self.n
        for port in range(len(self.portswid)):
            if port != 0:
                self.portswid[port].set(0)
            
    def reset(self):
        self.n = 0
        self.j = 0
        self.presamp = 5
        self.enexp.delete(0, Tk.END)
        self.enexp.insert(0, 0)
        self.snexp.set(0)
        self.epresamp.delete(0, Tk.END)
        self.epresamp.insert(0, 5)
        self.widgetframe()
        
    def setparameters(self):
        self.parameters = []
        for exp in range(self.n):
            self.parameters.append([])
            self.parameters[exp] = [-1, -1, -1, -1, -1]
            self.parameters[exp][0] = self.widgets[exp].color.get()
            self.parameters[exp][1] = self.widgets[exp].getsamples()
            self.parameters[exp][2] = self.widgets[exp].amplitude.get()
            self.parameters[exp][3] = self.widgets[exp].offset.get()
            self.parameters[exp][4] = self.widgets[exp].gain.get()
        print self.parameters
        
    def getonports(self):
        self.onports = []
        for port in range(len(self.portswid)):
            value = self.portswid[port].check()
            if value:
                self.onports.append(self.portswid[port].port)
        
    def saveroot(self, event = None):
        self.setparameters()
        self.getonports()
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
            print "ports label"
            self.file.write("%s" % self.onports)
            print "ports"
            self.file.write("\nNumber of experiments:\n%s\n" % (self.n))
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
            self.widgets[exp].setsamples(self.parameters[exp][1])
            self.widgets[exp].setamplitude(self.parameters[exp][2])
            self.widgets[exp].setoffset(self.parameters[exp][3])
            self.widgets[exp].setgain(self.parameters[exp][4])
        
        #except:
            #print "Error while opening file."
    
    def analizeresults(self):
        pass
    
    def about(self):
        pass