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

ls=reg2.RunCmd("eeprom read 4f")        #read test SN number
value=ShowReturnList(ls)                #get value from 4f

if value==0 or value==255:              #if there is no SN and create new
    localtime = time.localtime(time.time())     #Get the time informatino
    #print("Local current time :", localtime)
    #print(str(localtime.tm_year)[2:4])
    mun=int(str(localtime.tm_year)[2:4])+128    #128(1000 0000) for black version
    mun2=str(hex(mun))
    ls=reg2.RunCmd("EEPROM write 4f "+str(mun2)) #and store year and black/white information in address 4f
    #print(localtime.tm_mon)
    ls=reg2.RunCmd("EEPROM write 50 "+str(localtime.tm_mon))        #and store month in address 50
    #print(localtime.tm_mday)
    ls=reg2.RunCmd("EEPROM write 51 "+str(localtime.tm_mday))       #and store day in address 51
    #print(localtime.tm_hour)
    ls=reg2.RunCmd("EEPROM write 52 "+str(localtime.tm_hour))       #and store hour in address 52
    #print(localtime.tm_min)
    ls=reg2.RunCmd("EEPROM write 53 "+str(localtime.tm_min))        #and store min in address 53
    #print(localtime.tm_sec)
    ls=reg2.RunCmd("EEPROM write 54 "+str(localtime.tm_sec))        #and store sec in address 54


ls=reg2.RunCmd("eeprom read 4f")
serial_mun=str(ShowReturnListHex(ls))[2:4]
ls=reg2.RunCmd("eeprom read 50")
serial_mun=serial_mun+str(ShowReturnListHex(ls))[2:4]
ls=reg2.RunCmd("eeprom read 51")
serial_mun=serial_mun+str(ShowReturnListHex(ls))[2:4]
ls=reg2.RunCmd("eeprom read 52")
serial_mun=serial_mun+str(ShowReturnListHex(ls))[2:4]
ls=reg2.RunCmd("eeprom read 53")
serial_mun=serial_mun+str(ShowReturnListHex(ls))[2:4]
ls=reg2.RunCmd("eeprom read 54")
serial_mun=serial_mun+str(ShowReturnListHex(ls))[2:4]

ls=reg2.RunCmd("eeprom read 55")        #read test block
SN=int(ShowReturnList(ls))                #get value from 55
        
print("VCResult:{0};{1}".format(serial_mun,SN))    #sent serial number to log file

'''uuid1=str(uuid.uuid4())
#print(str(uuid.uuid4())[:8])
print(uuid1)
print(uuid1[:2])
print(uuid1[2:4])
print(uuid1[4:6])
print(uuid1[6:8])'''


#ls=reg2.RunCmd("eeprom read 55")        #read test station block
#ShowReturnList(ls)                      #log test block to UTS/Kinetic
