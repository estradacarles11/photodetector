# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 16:06:19 2016

@author: Carles Estrada
"""

import classes.interface as interface

gui = interface.Interface()
gui.main()
try:
    for widget in gui.widgets:
            widget.disconnect()
except:
    pass