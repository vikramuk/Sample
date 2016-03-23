#!/usr/bin/python

import sys
import time
import usb.core
import visa

AGILENT_33220A= "USB0::0x0957::0x0407::MY44021621::0::INSTR"


def set_Values_USB(period):
    # Check for Device Availability
    try:
        rm = visa.ResourceManager()
        rm.list_resources()
        inst_33220A = rm.open_resource(AGILENT_33220A, read_termination="\r")
        inst_33220A.timeout = 25        
        #print ("Checking Device Number")
        #print(inst_33220A.query("*IDN?", delay=1))
        print ("Resetting the Device")
        print(inst_33220A.write("*RST"))     
        print ("Disable the Output")
        print(inst_33220A.write(":OUTP:STAT 0")) 
        print("Setting Frequency")
        time.sleep(0.05)
        print(inst_33220A.write(":SOUR:FREQ:CW 1.1512 MHZ"))        
        print("Setting Amplitude")
        time.sleep(0.05)
        print(inst_33220A.write(":SOUR:VOLT:LEV:IMM:AMPL 0.1 VPP"))        #:SOUR:VOLT:LEV:IMM:AMPL 0.1
        print ("Setting Cycle Phase")
        time.sleep(0.05)
        print (inst_33220A.write(":SOUR:BURS:PHAS 0 "))
        print ("Enable Burst State")
        time.sleep(0.05)
        print(inst_33220A.write(":SOUR:BURS:STAT 1"))  
        print ("Setting Burst Cycles")
        time.sleep(0.05)        
        print (inst_33220A.write(":SOUR:BURS:NCYC 50000"))
        print ("Setting Period to %.2f S" %float(period))
        time.sleep(0.05)
        print (inst_33220A.write(":SOUR:BURS:INT:PER %f S" %float(period)))        
        print ("Enable the Output")
        time.sleep(0.05)
        print(inst_33220A.write(":OUTP:STAT 1"))       
    #Fail Gracefully
    except IOError:
        print 'cannot Connect to Device: '+ AGILENT_33220A
    except Exception as e:
        print e
    else:
        print "Connection has been Closed"       

if __name__ == "__main__":
    set_Values_USB(0.8)


