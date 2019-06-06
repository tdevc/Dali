import time
#import uuid
import RobotRun as rr

#==============================================================================================================    
def ShowReturnList(ls):
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
            return int(dat,0)
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
reg2=rr.CLVRegCmd()                         #initial Lvreg
ls=reg2.RunCmd("testxu write a 8")          #Enter TEDmode for EEprom access

ls=reg2.RunCmd("eeprom write 7d FF")          #reset low byte VCM_cal data
ls=reg2.RunCmd("eeprom write 7e FF")          #reset high byte VCM_cal data

ls=reg2.RunCmd("eeprom write 86 00")          #image setting reset
ls=reg2.RunCmd("eeprom write 87 00")          #image setting reset

ls=reg2.RunCmd("pcxu write 11 1")          #device SW rest(replug)

time_start=int(time.time())
while True:
    ls=reg2.RunCmd("device read 6")          #read USB info
    PID=ShowReturnListHex(ls)             #get PID
    print(PID)
    time.sleep(0.5)
    if int(time.time())-time_start>5 or PID=='0X6D0493081900':
        break

ls=reg2.RunCmd("testxu write a 8")          #Enter TEDmode for EEprom access

ls=reg2.RunCmd("eeprom read 7d")        #low byte VCM_cal data
VCM_low=int(ShowReturnList(ls))                #get low byte VCM_cal data value

ls=reg2.RunCmd("eeprom read 7e")        #low byte VCM_cal data
VCM_high=int(ShowReturnList(ls))                #get low byte VCM_cal data value

        
print("VCResult:{0};{1}".format(VCM_low,VCM_high))    #sent serial number to log file
