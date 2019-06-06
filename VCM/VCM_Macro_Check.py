import cv2
import numpy as np 
import csv
import RobotRun as rr
#from scipy.fftpack import fft,ifft
#import matplotlib.pyplot as plt
import time
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import os
import serial
IsimageOK=111
motorGoF=0
motorstatus=1
VCM_pos=0
#==============================================================================================================    
def PicProcessing_MTF():
    ROIX=int(200)
    ROIY=int(100)
    MTF_ave=0
    ROI_width=250
    ROI_height=1
    image = cv2.imread("image2.BMP")#读取图像

    for i in range(ROI_height):
        MTF=Pixelvalue(image,ROIX,ROIY+i,ROI_width)
        print(MTF)
        MTF_ave=MTF_ave+MTF/ROI_height

    cv2.rectangle(image, (ROIX, ROIY), (ROIX+ROI_width, ROIY+ROI_height), (0, 200, 0), 1)
    cv2.putText(image, str(round(MTF_ave,3)), (ROIX+40, ROIY-10), cv2.FONT_HERSHEY_DUPLEX,
                0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imshow('test',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#==============================================================================================================    
def stream_MTF(image,ROIX,ROIY):
    MTF_ave=0
    ROI_width=250       #ROI_width
    ROI_height=20       #ROI_height

    for i in range(ROI_height):
        MTF=Pixelvalue(image,ROIX,ROIY+i,ROI_width)
        #print(MTF)
        MTF_ave=MTF_ave+MTF/ROI_height

    cv2.rectangle(image, (ROIX, ROIY), (ROIX+ROI_width, ROIY+ROI_height), (0, 200, 0), 1)
    cv2.putText(image, str(round(MTF_ave,3)), (ROIX+40, ROIY-10), cv2.FONT_HERSHEY_DUPLEX,
                0.5, (0, 255, 0), 1, cv2.LINE_AA)
    #cv2.imshow('test',image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return MTF_ave
#=================================================================================================================
def Pixelvalue(image,ROIX,ROIY,ROI_width):
    Y = np.random.random(ROI_width)
    tempMax = np.random.random(50)  #line pair number
    tempMin = np.random.random(50)
    
    #f = open('pixelValue.csv', 'w')
    #ff = open('Max.csv', 'w')

    for i in range(ROI_width):
        PixelValue = image[ROIY,ROIX+i]#读取(0,0)像素，Python中图像像素是按B,G,R顺序存储的
        Y[i]=int(PixelValue[2])*0.299+int(PixelValue[1])*0.587+int(PixelValue[0])*0.114
        #f.write(str(PixelValue[0])+','+str(PixelValue[1])+','+str(PixelValue[2])+','+str(Y[i])+'\n')

    j=0
    MTF=0
    for k in range(2,ROI_width-10):
        if Y[k-1]<Y[k] and Y[k-2]<Y[k] and Y[k+1]<Y[k] and Y[k+2]<Y[k]:# and Y[k]<230 and Y[k]>30: #max white under 210 and over 30
            minpeak=min(Y[k+2], Y[k+3], Y[k+4])
            maxpeak=max(Y[k+5], Y[k+6], Y[k+7], Y[k+8], Y[k+9])
            if abs(minpeak-maxpeak)>30:
                tempMin[j]=minpeak
                #ff.write(str(tempMin[j])+',')
                tempMax[j]=maxpeak
                #ff.write(str(tempMax[j])+'\n')
                j=j+1

    for L in range(j):
        MTF_temp=(tempMax[L]-tempMin[L])/(tempMax[L]+tempMin[L])
        MTF=MTF+MTF_temp/j

    if j<3:
        MTF=0

    #ff.write(str(MTF)+'\n')
        
    #f.close()
    #ff.close()

    return MTF

#==============================================================================================================    
def initialsetting(VF):
    #rr.PropertySet2(0,3, 400)  #zoom
    #time.sleep(5)
    reg2=rr.CLVRegCmd()         #enable Lvreg
    ls=reg2.RunCmd("videoxu write 2 1") #viewport
    ls=reg2.RunCmd("videoxu write 7 0") #eis off
    rr.PropertySetAuto(0,6, 0)  #disable AF
    time.sleep(0.3)
    rr.PropertySet2(0, 4, -7)    #Exposure value
    time.sleep(0.3)
    rr.PropertySet2(0, 6, 0)    #focus value
    time.sleep(0.3)
    rr.PropertySet2(1, 9, 10)    #Gain value
    time.sleep(0.3)

#==============================================================================================================    
def askyesno_handler():
    global IsimageOK
    a=mb.askyesno("askyesno", "This is askyesno!")
    print(a)
    if a==1:
        IsimageOK=111
        return a
#============================================================================================================== 
def job():
    dialogreturn=askyesno_handler()
    if dialogreturn==1:
        print(dialogreturn)
        return dialogreturn
#============================================================================================================== 
def job2():
    global motorGoF
    global motorstatus
    global VCM_pos
    #print("motorstatus",motorstatus)
    while ( motorstatus==1):
        #print('motorGoF1',motorGoF)
        if motorGoF==1:
            rr.PropertySet2(0, 6, VCM_pos)    #focus value
            time.sleep(0.5)
            motorGoF=0
            #print(motorGoF)
#==============================================================================================================
def coarse_MTF():
    global motorGoF
    global motorstatus
    global VCM_pos
    Drive_mode=0
    VCM_MTF_Max=0
    VCM_Peak_pos=0
    VCM_MTF = np.random.random(50)
    
    cf=rr.CVideoFrame() # create video frame instance to handle "negative video
    p=0
    time_start=int(time.time())
    
    while True:
        MTF_far=0
        MTF_near=0
        FrameSource=rr.VideoFrameGet("")
        cf.VideoFrameSet(FrameSource)

        if IsimageOK==111:
            image = FrameSource

            #Far MTF (start position (200,50))
            MTF_far=round(stream_MTF(image,200,50)*100,2)
            #Near MTF (start position (200,400))
            MTF_near=round(stream_MTF(image,200,400)*100,2)
            #Delta calculated
            if MTF_far+MTF_near==0:
                MTF_far=1
            #Delta=round((MTF_far-MTF_near)/(MTF_far+MTF_near)*100,2)
            #cv2.putText(image, str(round(Delta,3)), (200, 220), cv2.FONT_HERSHEY_DUPLEX,
                        #0.5, (0, 255, 0), 1, cv2.LINE_AA)
            
            cf.VideoShow('Frame Video')
            
            if motorGoF==0:
                if VCM_pos<31:                   #from VCM table
                    Drive_mode=VCM_pos*5.46     #from VCM table
                else:                                       #from VCM table
                    Drive_mode=163.8+2.35*(VCM_pos-30)     #from VCM table
                print(MTF_far,MTF_near,VCM_pos,Drive_mode)
                VCM_MTF[p]=MTF_far
                VCM_pos=VCM_pos+5
                p=p+1
                motorGoF=1
  
            #moving lens to +
            #askyesno_handler()
            #print(MTF_far,MTF_near,Delta)
            #print('motorGoF2',motorGoF)
            #p=p+1
            #print(p)
            if VCM_pos>130:          # drive VCM 30 step
                print(int(time.time())-time_start)
                break

    motorstatus=0
    for k in range(1,50):
        if VCM_MTF_Max<=VCM_MTF[k]:
            VCM_MTF_Max=VCM_MTF[k]
            VCM_Peak_pos=k*5
            if VCM_Peak_pos<31:
                Drive_mode=round(VCM_Peak_pos*5.46,0)
            else:
                Drive_mode=round(163.8+2.35*(VCM_Peak_pos-30),0)

    #VCM_cal_data=hex((int(Drive_mode))-211 & (2**16-1))
    #print(VCM_MTF_Max,VCM_Peak_pos,Drive_mode,VCM_cal_data[4:6],VCM_cal_data[2:4])
    print("VCResult:{0} ;{1}".format(VCM_MTF_Max,VCM_Peak_pos))
    time.sleep(1)

#==============================================================================================================
def Stream():
    global motorGoF
    global motorstatus

    VF={"Format":"YUY2", "Resolution":"640x480", "FrameRate":30.0}
    #if not rr.PreviewStart(VF): return False
    
    rr.PreviewStart(VF)
    print("IsPreviewing="+str(rr.IsPreviewing()))
    #cf=rr.CVideoFrame() # create video frame instance to handle "negative video
    rr.Sleep(4000)
    #image initial
    initialsetting(VF)

    #rr.SetLensControlFamily("Bolide")
    #t1 = threading.Thread(target = job)  # 建立一個子執行緒 dialog box
    #t1.start()   # 執行該子執行緒

    t = threading.Thread(target = job2)  # Motor control
    t.start()   # 執行該子執行緒

    #t_MTF = threading.Thread(target = Job_MTF)  # 建立一個子執行緒
    #t_MTF.start()   # 執行該子執行緒
    coarse_MTF()

    '''p=0
    while True:
        MTF_far=0
        MTF_near=0
        FrameSource=rr.VideoFrameGet("")
        cf.VideoFrameSet(FrameSource)

        if IsimageOK==111:
            #t.join()   # 等待 t 這個子執行緒結束
            image = FrameSource

            #Far MTF (start position (200,50))
            MTF_far=stream_MTF(image,200,50)*100
            #Near MTF (start position (200,400))
            MTF_near=stream_MTF(image,200,400)*100
            #Delta calculated
            if MTF_far+MTF_near==0:
                MTF_far=1
            Delta=(MTF_far-MTF_near)/(MTF_far+MTF_near)*100
            cv2.putText(image, str(round(Delta,3)), (200, 220), cv2.FONT_HERSHEY_DUPLEX,
                        0.5, (0, 255, 0), 1, cv2.LINE_AA)
  
            cf.VideoShow('Frame Video')
            #moving lens to +
            #askyesno_handler()
            #print(MTF_far,MTF_near,Delta)
            motorGoF=1
            p=p+1
            print(p)
            if p>500:
                break'''

    #motorstatus=0
    #print(motorstatus)
    #t1.join()   # 等待 t 這個子執行緒結束
    t.join()   # 等待 t 這個子執行緒結束
    #t_MTF.join()   # 等待 t 這個子執行緒結束

    rr.PreviewStop()
#==============================================================================================================    
def ShowReturnListHex(ls):
    i=0
    #print("The output into a Python List as below:\n{}".format(ls))
    #print("Size Of Output List=",len(ls))
    for dat in ls:
        i=i+1
        if not dat=="":
            #print("({}).Return Data in Hex: {}".format(i,dat))
            #print("VCResult:{0}".format(dat))
            #print("({}).Return Data in decimal: {}".format(i,int(dat,0)))
            #print("VCResult:{0}".format(int(dat,0)))
            return dat
#============================================================================================================== 
def RE_emun():
    reg2=rr.CLVRegCmd() 
    ls=reg2.RunCmd("pcxu write 11 1")          #device SW rest(replug)
    time_start=int(time.time())
    while True:
        ls=reg2.RunCmd("device read 6")          #read USB info
        PID=ShowReturnListHex(ls)             #get PID
        print(PID)
        time.sleep(0.5)
        if int(time.time())-time_start>5 or PID=='0X6D0493081900':
            break
#============================================================================================================== 

if(__name__)=="__main__":
    RE_emun()
    #ser = serial.Serial('COM5', 9600, timeout=1)    #open serial comport
    #ser.readline()
    Stream()
    #ser.close() #close comport
    #PicProcessing_MTF()
