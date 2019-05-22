"""
Created on Thu Sep 08 12:13:52 2016

@author: Carles Estrada
"""

import sys 
import classes.photodetector as photodetector

class Experiment(object):
    def __init__(self):
        self.col = -1
        self.amp = -1
        self.off = -1
        self.ga = -1
        self.max_amp = 2.2
        self.max_off = 2.75
        self.max_ga = 2.75
        self.min_off = 0.85
        self.parameters = []
        self.exptype = 0
        self.n = 0
        self.newp = [2, 0.023, 0.85, 2]
        self.ph = photodetector.photodetector()
                
    def newexperiment(self):
        print "New Experiment!"
        # Establishing Connection
        self.ph.connectarduino('COM7')
        self.filename = 'C:\Users\user\Desktop\Carles\Experiments\%s.txt' % raw_input("File name: ")
        self.file = open(self.filename, 'w')
        self.setparameters()
        for i in self.parameters:
            self.oldp = self.newp
            self.newp = i
            self.ph.sendparameters(self.oldp, self.newp)
            self.ph.record(self.n + 2)
        self.writefile()
        self.ph.restart()
        self.file.close()
        self.ph.disconnectarduino()
        sys.exit()
        
    def setparameters(self):
        while self.exptype not in [1, 3]:
            self.exptype = raw_input("Single(S) or multiple(M) experiment? ")
            if (self.exptype == "Single" or self.exptype == "single" or self.exptype == "S" or self.exptype == "s"):
                self.exptype = 1
                self.setcolor()
                self.setamplitude()
                self.setgain()
                self.parameters.append([self.col, self.amp, self.off, self.ga])
                                
            elif (self.exptype == "Multiple" or self.exptype == "multiple" or self.exptype == "M" or self.exptype == "m"):
                self.exptype = 3
                print "For red:"
                self.max_amp = 1.1
                self.max_off = 2.046
                self.setamplitude()
                self.setgain()
                self.parameters.append([2, self.amp, self.off, self.ga])
                self.off = -1
                print "For green:"
                self.max_amp = 0.242
                self.max_off = 1.958
                self.setamplitude()
                self.setgain()
                self.parameters.append([1, self.amp, self.off, self.ga])
                self.off = -1
                print "For blue:"
                self.max_amp = 1.1
                self.max_off = 2.046
                self.setamplitude()
                self.setgain()
                self.parameters.append([0, self.amp, self.off, self.ga])
                self.off = -1
            print self.parameters
            while self.n < 1:
                self.n = int(raw_input("Number of measurements for each experiment: "))
    
    def setcolor(self):
        while self.col not in range(3):
            self.col = raw_input("Color (Red, Green or Blue): ")
            if self.col == "Blue" or self.col == "blue" or self.col == "B" or self.col == "b":
                self.color = "blue"
                self.col = 0
                self.max_amp = 1.1
                self.max_off = 2.046
            elif self.col == "Green" or self.col == "green" or self.col == "G" or self.col == "g":
                self.color = "green"
                self.col = 1
                self.max_amp = 0.242
                self.max_off = 1.958
            elif self.col == "Red" or self.col == "red" or self.col == "R" or self.col== "r":
                self.color = "red"
                self.col = 2
                self.max_amp = 1.1
                self.max_off = 2.046
        
        self.ph.sendcol(self.col, self.col)
        print "Color %s established!" % self.color
        
        return self.col
            
    def setamplitude(self):
        self.amp = -1
        while (self.amp < 0.023 or self.amp > self.max_amp):
            self.amp = float(raw_input("Amplitude (0.023V - %sV): " % self.max_amp))
        self.ph.sendamp(self.amp, self.col)
        print "Amplitude %sV established!" % self.amp
        if self.off == -1:
            self.setoffset()
        else:
            while (self.amp + self.off > 2.75 or self.off - self.amp < 0):
                print "Amplitude too large for this offset. Set offset again:"
                self.setoffset()
        return self.amp
    
    def setoffset(self):
        self.off = -1
        if self.max_off + self.amp > 2.75:
            self.max_off = 2.75 - self.amp
            self.min_off = 0.85
        elif self.amp > 0.85:
            self.min_off = self.amp
        while (self.off < self.min_off or self.off > self.max_off):
            self.off = float(raw_input("Offset (%sV - %sV): " % (self.min_off, self.max_off)))
        self.ph.sendoff(self.off, self.col)
        print "Offset %sV established!" % self.off
        return self.off
            
    def setgain(self):
        self.ga = -1
        while (self.ga < 0 or self.ga > self.max_ga):
            self.ga = float(raw_input("Gain (0V - %sV): " % self.max_ga))
        self.ph.sendga(self.ga, self.col)
        print "Gain %sV established!" % self.ga
        return self.ga
        
    def writefile(self):
        for i in self.ph.output:
            self.file.write("%s\n" % i)
            #self.file.write("b\'\\%s\n" % "\\x".join("{:02x}".format(ord(c)) for c in i))

    def analizeresults(self, name):
        pass

ex=Experiment()
ex.newexperiment()
#ex.analizeresults(filename)


