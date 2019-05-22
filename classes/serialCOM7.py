# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 12:15:49 2017

@author: user
"""
import serial

try:
    s = serial.Serial('COM7')
    print "opened"
    s.close()
    print "closed"
except:
    raise serial.SerialException("Could not open port COM7")