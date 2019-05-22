# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""

import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler


from matplotlib.figure import Figure
import Tkinter as Tk
import sys
sys.path.insert(0, '/ps')
import serial

        
def ReadFile(name):
    f=open(name,'r')

    d=f.readlines()

    k=[]
    for i in d:
        l=i.split()
        k.append(float(l[1]))
        print i,l

    print k
    return k


def NewFile():
    print "New File!"

    ser = serial.Serial(
    port='COM7')
    ser.write(b"\x02\x80\x80\x80")
    ser.write(b"\x0e\x80\x80\x80")
    
    for i in range(10):
      #  print ser.readline()
        print i
    
    
def OpenFile():
    name = askopenfilename()
    print name
    r=ReadFile(name)
    print r
    f = Figure(figsize=(5,5))
    
    plt.plot(range(len(r)),r,'r')
    plt.title("Grafica")
    plt.show()
    a=  f.add_subplot(111)
    a.plot(range(len(r)),r,'r')
#    plt.savefig("p1.pdf",format="pdf")
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    
root = Tk.Tk()
root.wm_title("Embedding in TK")

menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile)
filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

mainloop()
