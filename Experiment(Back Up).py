# -*- coding: utf-8 -*-
"""
Experiment

Created on Thu Sep 08 12:13:52 2016

@author: Carles Estrada
"""

import serial, sys, struct, time
"""
class Experiment(object,detector):
    def  __init__(self):
        self.detector=detector
 """   
        
class Experiment(object):
    def __init__(self, serport):
        
        self.serport = serport
        self.col = -1
        self.amp = -1
        self.off = -1
        self.ga = -1
        self.max_amp = 2.2
        self.max_off = 2.75
        self.max_ga = 2.75
        self.min_off = 0.85
        self.parameters = []
        self.output = []
        self.exptype = 0
        self.newp = [2, 0.023, 0.85, 2]
        
    def newexperiment(self):
        print "New Experiment!"
        # Establishing Connection
        self.connectarduino()
        #filename = raw_input("File name: ")
        self.filename = 'C:\Users\user\Desktop\Carles\Experiments\%s.txt' % raw_input("File name: ")
        self.file = open(self.filename, 'w')
        
        #Seting parameters
        self.n = int(raw_input("Number of measurements for each experiment: "))
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
            
        for i in self.parameters:
            self.oldp = self.newp
            self.newp = i
            self.sendparameters(self.oldp, self.newp)
            self.startrecording()
            
            
            """
            for i in range(self.exptype):
                self.sendcol(self.parameters[i+1][0], self.parameters[i][0])
                time.sleep(1)
                self.sendamp(self.parameters[i][1], self.parameters[i][0])
                time.sleep(1)
                self.sendoff(self.parameters[i][2], self.parameters[i][0])
                time.sleep(1)
                self.sendga(self.parameters[i][3], self.parameters[i][0])
                print "Parametes sent!"
                print self.parameters[i]
                self.startrecording()
            """
                
        self.writefile()
        self.file.close()
        self.disconnectarduino()
        sys.exit()
        
    def connectarduino(self):
        self.arduino = serial.Serial(
        port = self.serport,
        baudrate = 115200,
        timeout = 2)
        print "Successful Connection!"
        
    def disconnectarduino(self):
        self.arduino.close()
    
    def sendparameters(self, old, new):
        self.sendcol(old[0], new[0])
        time.sleep(1)
        self.sendamp(new[1], new[0])
        time.sleep(1)
        self.sendoff(new[2], new[0])
        time.sleep(1)
        self.sendga(new[3], new[0])
    
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
        
        self.sendcol(self.col, self.col)
        print "Color %s established!" % self.color
        
        return self.col
            
    def setamplitude(self):
        self.amp = -1
        while (self.amp < 0.023 or self.amp > self.max_amp):
            self.amp = float(raw_input("Amplitude (0.023V - %sV): " % self.max_amp))
        self.sendamp(self.amp, self.col)
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
        self.sendoff(self.off, self.col)
        print "Offset %sV established!" % self.off
        return self.off
            
    def setgain(self):
        self.ga = -1
        while (self.ga < 0 or self.ga > self.max_ga):
            self.ga = float(raw_input("Gain (0V - %sV): " % self.max_ga))
        self.sendga(self.ga, self.col)
        print "Gain %sV established!" % self.ga
        return self.ga
        
    def sendcol(self, old, new):
        self.arduino.write(struct.pack('bb', old, 14))
        time.sleep(1)
        self.arduino.write(struct.pack('bb', new, 10))
    
    def sendamp(self, amplitude, color):
        amp = int((amplitude - 0.022) * 2048 / 2.178 - 1)
        ampa = struct.pack('bbh', color, 11, amp)
        ampa = ampa[::-1]
        ampa = ampa.replace(ampa[0], "*", 1).replace(ampa[1], ampa[0], 1).replace("*", ampa[1], 1)
        ampa = ampa[::-1]
        #print "b\'\\%s" % "\\x".join("{:02x}".format(ord(c)) for c in ampa)
        self.arduino.write(ampa)
        
    def sendoff(self, offset, color):
        off = int((offset - 0.572) * 4096 / 2.178)
        offa = struct.pack('bbh', color, 12, off)
        offa = offa[::-1]
        offa = offa.replace(offa[0], "*", 1).replace(offa[1], offa[0], 1).replace("*", offa[1], 1)
        offa = offa[::-1]
        #print "b\'\\%s" % "\\x".join("{:02x}".format(ord(c)) for c in offa)
        self.arduino.write(offa)
        
    def sendga(self, gain, color):
        pass
        """
        ga = int(gain * 4096 / 2.75)
        gaa = struct.pack('bbh', color, 13, ga)
        gaa = gaa[::-1]
        gaa = gaa.replace(gaa[0], "*", 1).replace(gaa[1], gaa[0], 1).replace("*", gaa[1], 1)
        gaa = gaa[::-1]
        #print "b\'\\%s" % "\\x".join("{:02x}".format(ord(c)) for c in gaa)
        self.arduino.write(gaa)
        """
    
    def startrecording(self):
        print "Recording..."
        self.arduino.write(b'\x0E\x00\x00\x00')
        count = self.n + 2
        while count:
            self.output.append(self.arduino.read(4))
            print count
            count -= 1
        self.arduino.write(b'\x0F\x00\x00\x00')
        
        return self.output
        
    def writefile(self):
        count = self.exptype
        while count:
            for i in range(self.n + 2):
                self.file.write("b\'\\%s\n" % "\\x".join("{:02x}".format(ord(c)) for c in self.output[i]))
            count -= 1

    def analizeresults(self, name):
        pass

#try:

ex=Experiment('COM7')
ex.newexperiment()
#ph.analizeresults(filename)
#except:
    #print sys.exc_info()[0]
    #ph.arduino.close()

