import sys

#num1=int(sys.argv[1])
#num2=int(sys.argv[2])
#op=int(sys.argv[3])
num1=1
num2=2
op=1
if op==1: 
 result=num1+num2 
 print("kay{0} ;{1} ;{2}".format(result, num1, num2))
 print("kay{0} ;{1} ;{2}".format(result, num1, num2))
elif op==2: 
 result=num1-num2 
 print("{0} ;{1} ;{2}".format(result, num1, num2))
elif op==3: 
 result=num1*num2 
 print("{0} ;{1} ;{2}".format(result, num1, num2))
else: 
 result=num1*1.0/num2 
 print("{0}".format(result))
