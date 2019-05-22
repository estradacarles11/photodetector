"""
Created on Fri Sep 30 11:18:37 2016

@author: Carles Estrada
"""

import Tkinter as Tk

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
        self.wcolor(1)
        self.wamplitude(2)
        self.woffset(3)
        self.wgain(4)
    
    def wcolor(self, nrow):
        self.color = Tk.IntVar()
        lcolor = Tk.Label(self.lexp, text = "Color:")
        lcolor.grid(row = nrow, column = 0, sticky = Tk.W + Tk.E)
        self.rred = Tk.Radiobutton(self.lexp, text= "Red", indicatoron = 0, variable = self.color, value = 2, command = self.getcolor)
        self.rred.grid(row = nrow, column = 1, sticky = Tk.W + Tk.E)
        self.rgreen = Tk.Radiobutton(self.lexp, text= "Green", indicatoron = 0, variable = self.color, value = 1, command = self.getcolor)
        self.rgreen.grid(row = nrow, column = 2, sticky = Tk.W + Tk.E)
        self.rblue = Tk.Radiobutton(self.lexp, text= "Blue", indicatoron = 0, variable = self.color, value = 0, command = self.getcolor)
        self.rblue.grid(row = nrow, column = 3, sticky = Tk.W + Tk.E)
    
    def wamplitude(self, nrow):
        self.amplitude = Tk.DoubleVar()
        lamp = Tk.Label(self.lexp, text = "Amplitude:")
        lamp.grid(row = nrow, column = 0, sticky = "W")
        self.samp = Tk.Scale(self.lexp, variable = self.amplitude, from_ = self.minamp, to = self.maxamp, showvalue = 0, orient = Tk.HORIZONTAL, resolution = 0.001, length = 150, command = self.getamplitude)
        self.samp.grid(row = nrow, column = 1, sticky = "W", columnspan = 3)
        self.eamp = Tk.Entry(self.lexp, width = 6)
        self.eamp.grid(row = nrow, column = 4, sticky = "W")
        checkbutton = Tk.Button(self.lexp, text = "Check", command = self.geteamp)
        checkbutton.grid(row = nrow, column = 5, sticky = Tk.E + Tk.W)
        
    def woffset(self, nrow):
        self.offset = Tk.DoubleVar()
        loff = Tk.Label(self.lexp, text = "Offset:")
        loff.grid(row = nrow, column = 0, sticky = "W")
        self.soff = Tk.Scale(self.lexp, variable = self.offset, from_ = self.minoff, to = self.maxoff, showvalue = 0, orient = Tk.HORIZONTAL, resolution = 0.001, length = 150, command = self.getoffset)
        self.soff.grid(row = nrow, column = 1, sticky = "W", columnspan = 3)
        self.eoff = Tk.Entry(self.lexp, width = 6)
        self.eoff.grid(row = nrow, column = 4, sticky = "W")
        checkbutton = Tk.Button(self.lexp, text = "Check", command = self.geteoff)
        checkbutton.grid(row = nrow, column = 5, sticky = Tk.E + Tk.W)
    
    def wgain(self, nrow):
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
        off = float(self.offset.get())
        if off + amp > 2.75:
            maxoffset = 2.75 - amp
            if maxoffset < self.maxoff:
                self.maxoff = maxoffset
                self.soff.config(to = self.maxoff)
        else:
            self.getcolor()
        self.eamp.delete(0, Tk.END)
        self.eamp.insert(0, amp)
    
    def geteamp(self):
        amp = float(self.eamp.get())
        if amp > self.maxamp or amp < self.minamp:
            self.eamp.delete(0, Tk.END)
        else:
            self.samp.set(amp)
            self.getamplitude()
        
    def getoffset(self, o):
        off = float(o)
        amp = float(self.amplitude.get())
        if amp + off > 2.75:
            maxamplitude = 2.75 - off
            if maxamplitude < self.maxamp:
                self.maxamp = maxamplitude
                self.samp.config(to = self.maxamp)
        else:
            self.getcolor()
        self.eoff.delete(0, Tk.END)
        self.eoff.insert(0, off)
    
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
    
    def getega(self):
        ga = float(self.ega.get())
        if ga > self.maxga or ga < self.minga:
            self.ega.delete(0, Tk.END)
        else:
            self.sga.set(ga)
            self.getgain()
        
    def expframegrid(self, row, column):
        self.lexp.grid(row = row, column = column, sticky = "W")
        
    def setcolor(self, color):
        #self.color = color
        print isinstance(color, int)
        if color == 0:
            print color
            self.rblue.invoke()
        elif color == 1:
            self.rgreen.invoke()
        elif color == 2:
            self.rred.invoke()
        print color
        
    def setamplitude(self, amp):
        #self.amplitude = amplitude
        self.samp.set(amp)
        
    def setoffset(self, off):
        #self.offset = offset
        self.soff.set(off)
        
    def setgain(self, ga):
        #self.gain = gain
        self.sga.set(ga)