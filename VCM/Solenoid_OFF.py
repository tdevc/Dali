import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import serial
import time

#==============================================================================================================    
def askyesno_handler():
    a=mb.askyesno("電磁閥控制", "電磁閥復位?")
    print(a)
    if a==1:
        ser.write(b'RELAY_OFF\n')
        time.sleep(0.5)
    else:
        ser.write(b'RELAY_ON\n')
        time.sleep(0.5)

#==============================================================================================================    
ser = serial.Serial('COM5', 9600, timeout=1)    #open serial comport
ser.readline()

askyesno_handler()

ser.close() #close comport
