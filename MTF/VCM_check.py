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
from sys import exit
IsimageOK=0
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
    exit(0)
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
            if abs(minpeak-maxpeak)>20:
                tempMin[j]=minpeak
                #ff.write(str(tempMin[j])+',')
                tempMax[j]=maxpeak
                #ff.write(str(tempMax[j])+'\n')
                j=j+1

    for L in range(j):
        MTF_temp=(tempMax[L]-tempMin[L])/(tempMax[L]+tempMin[L])
        MTF=MTF+MTF_temp/j

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
    rr.PropertySetAuto(0,6, 0)  #disable AF
    time.sleep(0.3)
    rr.PropertySet2(0, 4, -7)    #Exposure value
    time.sleep(0.3)
    rr.PropertySet2(0, 6, 200)    #focus value
    time.sleep(0.5)
    rr.PropertySet2(1, 9, 105)    #Gain value
    time.sleep(0.3)
#==============================================================================================================    
def VCM_setting(VF):
    rr.PropertySet2(0, 6, 200)    #focus value
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
def VCM_test():
    VF={"Format":"YUY2", "Resolution":"640x480", "FrameRate":30.0}
    #if not rr.PreviewStart(VF): return False
    
    rr.PreviewStart(VF)
    print("IsPreviewing="+str(rr.IsPreviewing()))
    cf=rr.CVideoFrame() # create video frame instance to handle "negative video
    rr.Sleep(4000)
    #VCM to macro
    initialsetting(VF)
    rr.Sleep(3000)

    p=0
    #rr.SetLensControlFamily("Bolide")
    #t = threading.Thread(target = job)  # 建立一個子執行緒
    #t.start()   # 執行該子執行緒

    while True:
        p=p+1

        MTF_near=0
        FrameSource=rr.VideoFrameGet("")
        cf.VideoFrameSet(FrameSource)

        image = FrameSource


        #Near MTF (start position (200,400))
        MTF_near=stream_MTF(image,200,400)*100
  
        cf.VideoShow('Frame Video')

        if p>150 or IsimageOK==111:
            cf.VideoFrameSave("C:\\Temp\\VCM.bmp")
            break

    #t.join()   # 等待 t 這個子執行緒結束
    print("VCResult:{0}".format(MTF_near))
    rr.PreviewStop()
#=================================================================================================================
if(__name__)=="__main__":
    #PicProcessing_MTF()
    VCM_test()
