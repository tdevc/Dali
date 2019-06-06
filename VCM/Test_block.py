import RobotRun as rr

reg2=rr.CLVRegCmd()                         #initial Lvreg
ls=reg2.RunCmd("eeprom write 55 4")        #read test station block
