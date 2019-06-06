import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import serial
import time

#==============================================================================================================    
def askyesno_handler():
    ser.write(b'P7R')
    '''a=mb.askyesno("電磁閥控制", "電磁閥復位?")
    #print(a)
    if a==1:
        ser.write(b'P7L')
        time.sleep(0.5)
    else:
        ser.write(b'P7H')
        time.sleep(0.5)'''

#==============================================================================================================    
ser = serial.Serial('COM10', 9600, timeout=1)    #open serial comport
ser.readline()

#askyesno_handler()
print('VCM_Cal_chart')
ser.close() #close comport
