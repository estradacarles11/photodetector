"""
Created on Fri Sep 30 11:18:37 2016

@author: Carles Estrada
"""

import serial, struct, time

class photodetector(object):
    def __init__(self):
        pass        
    def connectarduino(self, serport):
        try:
            self.serport = serport
            self.arduino = serial.Serial(
            port = self.serport,
            baudrate = 115200,
            timeout = 2)
            print "Successful Connection!"
        except:
            pass
        
    def disconnectarduino(self):
        try:
            self.arduino.close()
        except:
            pass
    
    def sendparameters(self, old, new):
        self.sendcol(old[0], new[0])
        time.sleep(1)
        self.sendamp(new[1], new[0])
        time.sleep(1)
        self.sendoff(new[2], new[0])
        time.sleep(1)
        self.sendga(new[3], new[0])
        
    def sendcol(self, old, new):
        try:
            self.arduino.write(struct.pack('bb', old, 14))
            time.sleep(1)
            self.arduino.write(struct.pack('bb', new, 10))
        except:
            pass
    
    def sendamp(self, amplitude, color):
        try:
            amp = int((amplitude - 0.022) * 2048 / 2.178 - 1)
            ampa = struct.pack('hbb', amp, 11, color)
            ampa = ampa[::-1]
            #ampa = ampa.replace(ampa[0], "*", 1).replace(ampa[1], ampa[0], 1).replace("*", ampa[1], 1)
            #ampa = ampa[::-1]
            #print "b\'\\x%s" % "\\x".join("{:02x}".format(ord(c)) for c in ampa)
            self.arduino.write(ampa)
        except:
            pass
        
    def sendoff(self, offset, color):
        try:
            off = int((offset - 0.572) * 4096 / 2.178)
            offa = struct.pack('hbb', off, 12, color)
            offa = offa[::-1]
            #offa = offa.replace(offa[0], "*", 1).replace(offa[1], offa[0], 1).replace("*", offa[1], 1)
            #offa = offa[::-1]
            #print "b\'\\x%s" % "\\x".join("{:02x}".format(ord(c)) for c in offa)
            self.arduino.write(offa)
        except:
            pass
        
    def sendga(self, gain, color):
        pass
        """
        ga = int(gain * 4096 / 2.75)
        gaa = struct.pack('bbh', color, 13, ga)
        gaa = gaa[::-1]
        gaa = gaa.replace(gaa[0], "*", 1).replace(gaa[1], gaa[0], 1).replace("*", gaa[1], 1)
        gaa = gaa[::-1]
        #print "b\'\\x%s" % "\\x".join("{:02x}".format(ord(c)) for c in gaa)
        self.arduino.write(gaa)
        """
    
    def record(self, count):
        self.restart()
        try:
            self.startrecording()
            self.arduino.read(1)
            while count:
                a = self.arduino.read(4)
                if int(struct.unpack('l', a)[0]) != 2573:
                    self.recorded.append(a)
                    #print count, str(struct.unpack('l', a)[0]), "b\'\\x%s" % "\\x".join("{:02x}".format(ord(c)) for c in a)
                    count -= 1
            for i in self.recorded:
                print "b\'\\x%s" % "\\x".join("{:02x}".format(ord(c)) for c in i)
                i = i[2:4]
                s = int(struct.unpack('h', i)[0])
                v = int(s * 3300 / 4096)
                print v, "mV", "b\'\\x%s" % "\\x".join("{:02x}".format(ord(c)) for c in i), "\n"
                self.output.append(v)
        except:
            print "Error while recording"
        self.stoprecording()
        return self.output
        
    def startrecording(self):
        self.arduino.write(b'\x0E\x00\x00\x00')
    
    def stoprecording(self):
        self.arduino.write(b'\x0F\x00\x00\x00')
    
    def restart(self):
        self.recorded = []
        self.output = []
        