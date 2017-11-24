# Import required modules
from Tkinter import *
import tkMessageBox
import os
import sys
import time
import struct
import array
import usb.core
import usb.util
from ContentCounter import ContentCounter
import threading

# Declare Global variables
os.environ['PYUSB_DEBUG'] = 'debug'
WORD_BYTES = 2
PARENT_HEADER_BYTES = 2 * WORD_BYTES
CHILD_HEADER_BYTES = 2 * WORD_BYTES
datadict = {}
datadictNovii = [dict() for i in range(10)]
datadictMX = {}
datadictIUPC = {}
datadictFECG = {}
datadictTOCO = {}
datadictNsatx = {}
datadictMECG = [dict() for i in range(125)]

class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError, "cannot use pack with this widget"
    def place(self, **kw):
        raise TclError, "cannot use place with this widget"

class Acs_Test_App(Frame):
    
    def __init__(self, master = None):
        Frame.__init__(self, master)
        
        self.master = master
        #self.master.title("ACS Test App")
        self.pack(fill=BOTH, expand=1)
        
        Label(self, padx=80, pady=20,text="ACS TEST APPLICATION", font= "Verdana 20 bold", fg="MediumSeaGreen", justify=CENTER).grid(row=0, columnspan=100)
                            
        # Variables to communicate with USB
        # TEMP
        self._dev = None
        self._ep = None     
        self._ep_read = None
        self._varList = {}
        self._columnCount = 1
        
        # NOVII
        self._dev_novii = None
        self.ep_novii = None
        self.ep_read_novii = None
        self._varListNovii = [dict() for i in range(10)]
        self._Novii_columnCount = 1
        self._rowCount = 3

        # MX
        self._dev_mx = None
        self.ep_mx = None
        self.ep_read_mx = None
        self._varListMX = {}
        self._MX_columnCount = 1
        self._MX_rowCount = 25

        # NSATX
        self._dev_nsatx = None
        self._ep_nsatx = None
        self._ep_read_nsatx = None
        self._varListNsatx = {}
        self._Nsatx_columnCount = 1
        self._Nsatx_rowCount = 95

        #MECG
        self._dev_mecg = None
        self._ep_mecg = None
        self._ep_read_mecg = None
        self._varListMECG = [dict() for i in range(125)]
        self._MECG_columnCount = 1
        self._MECG_rowCount =65

        #IUPC
        self._dev_iupc = None
        self._ep_iupc = None
        self._ep_read_iupc = None
        self._varListIUPC = {}
        self._IUPC_columnCount = 1
        self._IUPC_rowCount =125

        #FECG
        self._dev_fecg = None
        self._ep_fecg = None
        self._ep_read_fecg = None
        self._varListFECG = {}
        self._FECG_columnCount = 1
        self._FECG_rowCount =135

        #TOCO
        self._dev_toco = None
        self._ep_toco = None
        self._ep_read_toco = None
        self._varListTOCO = {}
        self._TOCO_columnCount = 1
        self._TOCO_rowCount =145
        
        
    def start_transaction(self):

        #Get the Device
        self._dev = usb.core.find(idVendor=0x1901, idProduct=0x0065)
        if self._dev == None:
            pass
        else:
            # set the active configuration. With no arguments, the first configuration will be the active one
            self._dev.set_configuration()
            # get actvie configuration
            cfg = self._dev.get_active_configuration()
            
            intf = cfg[(0,0)]
            self._ep = usb.util.find_descriptor(
                intf,
                # match the first OUT endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)
            assert self._ep is not None

            self._ep_read = usb.util.find_descriptor(
                intf,
                # match the first IN endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)

            assert self._ep_read is not None

            # Send Start up Request Packet
            datasend =  '\x30\x5E\xED\xBA\xDE\x00\x12\x00\x01\x1F\x5A\x00\x46\x00\x10\x00\x04\x00\x08\x2D\xEE\x5D\xCC\xAE\x2F\x85\xAD\xDC\x18\xA1\xF2\x2E\x87\x27\x79\x00\x0A\x00\x00\x00\x02\x00\x00\x00\x07\x00\x00\xAF\xD0'
            self._ep.write(datasend)

            while True:
                try:
                    # Get the Start up Response Packet.
                    data = self._ep_read.read(64)
                    #print data
                    # print ' '.join([hex(Byte)[2:] for Byte in data])
                    break
                except usb.core.USBError as e:
                    sys.exit("Could not read from endpoint: %s" % str(e))
            # Send Start up Complete Packet
            datawrite= '\x18\x5E\xED\xBA\xDE\x00\x06\x00\x02\xB0\x9A\x00\x46\x00\x04\x00\x0E\x00\x00\x00\x02\x00\x00\x75\x26'
            self._ep.write(datawrite)
            #Get Startup complete Response Packet.
            data = self._ep_read.read(64)
            # TEMP Thread
            threading.Thread(target=self.mycallback).start()
            time.sleep(1)
            

        #Noviiiiiiiiiiiii
        # find our device
        self._dev_novii = usb.core.find(idVendor=0x1901, idProduct=0x0066)
        #print dev
        # was it found?
        if self._dev_novii is None:
            pass
        else:
            # set the active configuration. With no arguments, the first configuration will be the active one
            self._dev_novii.set_configuration()
            # get an endpoint instance
            cfg_novii = self._dev_novii.get_active_configuration()
            intf_novii = cfg_novii[(0,0)]#usb.util.find_descriptor(cfg, bInterfaceNumber=2)
            self.ep_novii = usb.util.find_descriptor(
                intf_novii,
                # match the first OUT endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)
            assert self.ep_novii is not None

            self.ep_read_novii = usb.util.find_descriptor(
                intf_novii,
                # match the first IN endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)

            assert self.ep_read_novii is not None
            # Send Start up Request Packet
            datasend_novii =  '\x30\x5E\xED\xBA\xDE\x00\x12\x00\x01\x1F\x5A\x00\x46\x00\x10\x00\x04\x00\x08\xCD\x49\xBE\x53\x89\x99\x2D\x2C\x20\xB0\x7F\x65\xC5\x96\x9D\x7A\x00\x0A\x00\x00\x00\x02\x00\x00\x00\x07\x00\x00\xE8\x1C'
            self.ep_novii.write(datasend_novii)

            while True:
                try:
                    # Get the Start up Response Packet.
                    data_novii = self.ep_read_novii.read(64)
                    #print data
                    # print ' '.join([hex(Byte)[2:] for Byte in data])
                    break
                except usb.core.USBError as e:
                    sys.exit("Could not read from endpoint: %s" % str(e))
            # Send Start up Complete Packet
            datawrite_novii= '\x18\x5E\xED\xBA\xDE\x00\x06\x00\x02\xB0\x9A\x00\x46\x00\x04\x00\x0E\x00\x00\x00\x02\x00\x00\x75\x26'
            self.ep_novii.write(datawrite_novii)
            #Get Startup complete Response Packet.
            data_novii = self.ep_read_novii.read(64)
            # NOVII Thread
            threading.Thread(target=self.mycallback_novii).start()
            time.sleep(1)
        
        #MX
        self._dev_mx = usb.core.find(idVendor=0x1901, idProduct=0x0032)

        #print dev
        # was it found?
        if self._dev_mx is None:
            pass
        else:
            # set the active configuration. With no arguments, the first configuration will be the active one
            self._dev_mx.set_configuration()
            # get an endpoint instance
            cfg = self._dev_mx.get_active_configuration()
            intf = cfg[(0,0)]#usb.util.find_descriptor(cfg, bInterfaceNumber=2)
            self.ep_mx = usb.util.find_descriptor(
                intf,
                # match the first OUT endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)
            assert self.ep_mx is not None

            self.ep_read_mx = usb.util.find_descriptor(
                intf,
                # match the first IN endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)

            assert self.ep_read_mx is not None
            # Send Start up Request Packet
            datasend =  '\x30\x5E\xED\xBA\xDE\x00\x12\x00\x01\x1F\x5A\x00\x46\x00\x10\x00\x04\x00\x08\x13\xD0\xDD\x7E\x85\x14\x78\x10\xD6\x51\x17\x5F\xE2\x1B\x59\xE2\x00\x0A\x00\x00\x00\x02\x00\x00\x00\x07\x00\x00\x01\x86'
            self.ep_mx.write(datasend)

            while True:
                try:
                    # Get the Start up Response Packet.
                    data = self.ep_read_mx.read(64)
                    #print data
                    break
                except usb.core.USBError as e:
                    sys.exit("Could not read from endpoint: %s" % str(e))
            # Send Start up Complete Packet
            datawrite= '\x18\x5E\xED\xBA\xDE\x00\x06\x00\x02\xB0\x9A\x00\x46\x00\x04\x00\x0E\x00\x00\x00\x02\x00\x00\x75\x26'
            self.ep_mx.write(datawrite)
            #Get Startup complete Response Packet.
            data = self.ep_read_mx.read(64)
            # MX Thread
            threading.Thread(target=self.mycallback_MX).start()
            time.sleep(1)
        
        #MECG
        # find our device
        self._dev_mecg = usb.core.find(idVendor=0x1901, idProduct=0x0020)

        #print dev
        # was it found?
        if self._dev_mecg is None:
            pass
        else:
            # set the active configuration. With no arguments, the first configuration will be the active one
            self._dev_mecg.set_configuration()
            # get an endpoint instance
            cfg = self._dev_mecg.get_active_configuration()
            intf = cfg[(0,0)]#usb.util.find_descriptor(cfg, bInterfaceNumber=2)
            self._ep_mecg = usb.util.find_descriptor(
                intf,
                # match the first OUT endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)
            assert self._ep_mecg is not None

            self._ep_read_mecg = usb.util.find_descriptor(
                intf,
                # match the first IN endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)

            assert self._ep_read_mecg is not None
            # Send Start up Request Packet
            datasend =   '\x30\x5E\xED\xBA\xDE\x00\x12\x00\x01\x1F\x5A\x00\x46\x00\x10\x00\x04\x00\x08\xCD\x49\xBE\x53\x89\x99\x2D\x2C\x20\xB0\x7F\x65\xC5\x96\x9D\x7A\x00\x0A\x00\x00\x00\x02\x00\x00\x00\x07\x00\x00\xE8\x1C'
            self._ep_mecg.write(datasend)

            while True:
                try:
                    # Get the Start up Response Packet.
                    data = self._ep_read_mecg.read(64)
                    #print data
                    # print ' '.join([hex(Byte)[2:] for Byte in data])
                    break
                except usb.core.USBError as e:
                    sys.exit("Could not read from endpoint: %s" % str(e))
            # Send Start up Complete Packet
            datawrite= '\x18\x5E\xED\xBA\xDE\x00\x06\x00\x02\xB0\x9A\x00\x46\x00\x04\x00\x0E\x00\x00\x00\x02\x00\x00\x75\x26'
            self._ep_mecg.write(datawrite)
            #Get Startup complete Response Packet.
            data = self._ep_read_mecg.read(64)
            # MECG Thread
            threading.Thread(target=self.mycallback_mecg).start()
                
        #NSATX
        # find our device
        self._dev_nsatx = usb.core.find(idVendor=0x1901, idProduct=0x0033)

        #print dev
        # was it found?
        if self._dev_nsatx is None:
            pass
        else:            
            # set the active configuration. With no arguments, the first configuration will be the active one
            self._dev_nsatx.set_configuration()
            # get an endpoint instance
            cfg = self._dev_nsatx.get_active_configuration()
            intf = cfg[(0,0)]#usb.util.find_descriptor(cfg, bInterfaceNumber=2)
            self._ep_nsatx = usb.util.find_descriptor(
                intf,
                # match the first OUT endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)
            assert self._ep_nsatx is not None

            self._ep_read_nsatx = usb.util.find_descriptor(
                intf,
                # match the first IN endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)

            assert self._ep_read_nsatx is not None
            # Send Start up Request Packet
            datasend =  '\x30\x5E\xED\xBA\xDE\x00\x12\x00\x01\x1F\x5A\x00\x46\x00\x10\x00\x04\x00\x08\x10\x84\xA0\xBC\x74\xFE\xD0\x7D\x60\x1F\x09\xB4\x14\x59\x1D\xA0\x00\x0A\x00\x00\x00\x02\x00\x00\x00\x07\x00\x00\x39\x15'
            self._ep_nsatx.write(datasend)

            while True:
                try:
                    # Get the Start up Response Packet.
                    data = self._ep_read_nsatx.read(64)
                    #print data
                    # print ' '.join([hex(Byte)[2:] for Byte in data])
                    break
                except usb.core.USBError as e:
                    sys.exit("Could not read from endpoint: %s" % str(e))
            # Send Start up Complete Packet
            datawrite= '\x18\x5E\xED\xBA\xDE\x00\x06\x00\x02\xB0\x9A\x00\x46\x00\x04\x00\x0E\x00\x00\x00\x02\x00\x00\x75\x26'
            self._ep_nsatx.write(datawrite)
            #Get Startup complete Response Packet.
            data = self._ep_read_nsatx.read(64)
            # NSATX Thread
            threading.Thread(target=self.mycallback_nsatx).start()
            time.sleep(1)
            

        #IUPC
        # find our device
        self._dev_iupc = usb.core.find(idVendor=0x1901, idProduct=0x0064)

        #print dev
        # was it found?
        if self._dev_iupc is None:
            pass
        else:
            # set the active configuration. With no arguments, the first configuration will be the active one
            self._dev_iupc.set_configuration()
            # get an endpoint instance
            cfg = self._dev_iupc.get_active_configuration()
            intf = cfg[(0,0)]#usb.util.find_descriptor(cfg, bInterfaceNumber=2)
            self._ep_iupc = usb.util.find_descriptor(
                intf,
                # match the first OUT endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)
            assert self._ep_iupc is not None

            self._ep_read_iupc = usb.util.find_descriptor(
                intf,
                # match the first IN endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)

            assert self._ep_read_iupc is not None
            # Send Start up Request Packet
            datasend =  '\x30\x5E\xED\xBA\xDE\x00\x12\x00\x01\x1F\x5A\x00\x46\x00\x10\x00\x04\x00\x08\x17\x49\x31\x4E\x86\x92\x97\x6B\xCF\x98\xCE\xCC\x5C\x40\xCE\xFC\x00\x0A\x00\x00\x00\x02\x00\x00\x00\x07\x00\x00\xE8\xBB'
            self._ep_iupc.write(datasend)

            while True:
                try:
                    # Get the Start up Response Packet.
                    data = self._ep_read_iupc.read(64)
                    #print data
                    # print ' '.join([hex(Byte)[2:] for Byte in data])
                    break
                except usb.core.USBError as e:
                    sys.exit("Could not read from endpoint: %s" % str(e))
            # Send Start up Complete Packet
            datawrite= '\x18\x5E\xED\xBA\xDE\x00\x06\x00\x02\xB0\x9A\x00\x46\x00\x04\x00\x0E\x00\x00\x00\x02\x00\x00\x75\x26'
            self._ep_iupc.write(datawrite)
            #Get Startup complete Response Packet.
            data = self._ep_read_iupc.read(64)
            # IUPC Thread
            threading.Thread(target=self.mycallback_iupc).start()
            time.sleep(1)

        #FECG
        # find our device
        self._dev_fecg = usb.core.find(idVendor=0x1901, idProduct=0x0063)

        #print dev
        # was it found?
        if self._dev_fecg is None:
            pass
        else:
            # set the active configuration. With no arguments, the first configuration will be the active one
            self._dev_fecg.set_configuration()
            # get an endpoint instance
            cfg = self._dev_fecg.get_active_configuration()
            intf = cfg[(0,0)]#usb.util.find_descriptor(cfg, bInterfaceNumber=2)
            self._ep_fecg = usb.util.find_descriptor(
                intf,
                # match the first OUT endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)
            assert self._ep_fecg is not None

            self._ep_read_fecg = usb.util.find_descriptor(
                intf,
                # match the first IN endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)

            assert self._ep_read_fecg is not None
            # Send Start up Request Packet
            datasend =  '\x30\x5E\xED\xBA\xDE\x00\x12\x00\x01\x1F\x5A\x00\x46\x00\x10\x00\x04\x00\x08\xAA\xE3\x1B\xC2\x55\xB9\x0A\x53\x0E\x21\x3A\xBD\x1C\x0C\xC5\x1F\x00\x0A\x00\x00\x00\x02\x00\x00\x00\x07\x00\x00\x4A\xDF'
            self._ep_fecg.write(datasend)

            while True:
                try:
                    # Get the Start up Response Packet.
                    data = self._ep_read_fecg.read(64)
                    #print data
                    # print ' '.join([hex(Byte)[2:] for Byte in data])
                    break
                except usb.core.USBError as e:
                    sys.exit("Could not read from endpoint: %s" % str(e))
            # Send Start up Complete Packet
            datawrite= '\x18\x5E\xED\xBA\xDE\x00\x06\x00\x02\xB0\x9A\x00\x46\x00\x04\x00\x0E\x00\x00\x00\x02\x00\x00\x75\x26'
            self._ep_fecg.write(datawrite)
            #Get Startup complete Response Packet.
            data = self._ep_read_fecg.read(64)
            # IUPC Thread
            threading.Thread(target=self.mycallback_fecg).start()
            time.sleep(1)

        #TOCO
        # find our device
        self._dev_toco = usb.core.find(idVendor=0x1901, idProduct=0x0062)

        #print dev
        # was it found?
        if self._dev_toco is None:
            pass
        else:
            # set the active configuration. With no arguments, the first configuration will be the active one
            self._dev_toco.set_configuration()
            # get an endpoint instance
            cfg = self._dev_toco.get_active_configuration()
            intf = cfg[(0,0)]#usb.util.find_descriptor(cfg, bInterfaceNumber=2)
            self._ep_toco = usb.util.find_descriptor(
                intf,
                # match the first OUT endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)
            assert self._ep_toco is not None

            self._ep_read_toco = usb.util.find_descriptor(
                intf,
                # match the first IN endpoint
                custom_match=lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)

            assert self._ep_read_toco is not None
            # Send Start up Request Packet
            datasend =  '\x30\x5E\xED\xBA\xDE\x00\x12\x00\x01\x1F\x5A\x00\x46\x00\x10\x00\x04\x00\x08\x39\x1D\x33\xA9\x5C\x08\x62\xE2\xE8\x5B\x8C\x84\xE4\xB4\x81\x0D\x00\x0A\x00\x00\x00\x02\x00\x00\x00\x07\x00\x00\xB3\x06'
            self._ep_toco.write(datasend)

            while True:
                try:
                    # Get the Start up Response Packet.
                    data = self._ep_read_toco.read(64)
                    #print data
                    # print ' '.join([hex(Byte)[2:] for Byte in data])
                    break
                except usb.core.USBError as e:
                    sys.exit("Could not read from endpoint: %s" % str(e))
            # Send Start up Complete Packet
            datawrite= '\x18\x5E\xED\xBA\xDE\x00\x06\x00\x02\xB0\x9A\x00\x46\x00\x04\x00\x0E\x00\x00\x00\x02\x00\x00\x75\x26'
            self._ep_toco.write(datawrite)
            #Get Startup complete Response Packet.
            data = self._ep_read_toco.read(64)
            # IUPC Thread
            threading.Thread(target=self.mycallback_toco).start()
            time.sleep(1)
       
       
    def mycallback(self):
        Label(self, text="TEMP", padx=82, pady=20, relief=RIDGE, bg="MediumSeaGreen").grid(row=1,rowspan=2)
        # Old CRC
        old_crc = [0,0]
        newPacket = []
        while True:
            try:
                data = self._ep_read.read(self._ep_read.wMaxPacketSize)
                if data[1]==94 and data[2]==237:
                    newPacket = data[11:]
                    if newPacket[-2:]!=old_crc:
                        old_crc = newPacket[-2:]
                        pdata = ' '.join([format(Byte, '02x') for Byte in newPacket])
                        self.CheckAndPrint(bytearray.fromhex(pdata))
                else:
                    newPacket.extend(data[1:])
            except usb.core.USBError as e:
                #sys.exit("Could not read from endpoint: %s" % str(e))
                continue
            finally:
                #usb.util.dispose_resources(self._dev)
                #self._ep = None
                #self._ep_read = None
                pass
    def mycallback_novii(self):
        Label(self, text="NOVII", padx=82, pady=20, relief=RIDGE, bg="MediumSeaGreen").grid(row=3,rowspan=2)
        # Old CRC
        old_crc = [0,0]
        newPacket = []
        cnt=0
        while True:
            try:
                data = self.ep_read_novii.read(self.ep_read_novii.wMaxPacketSize, timeout=100000)  #  40000000
                if data[1]==94 and data[2]==237:
                    if len(newPacket)!=0:
                        if newPacket[-2:]!=old_crc:
                            old_crc = newPacket[-2:]
                            pdata = ' '.join([format(Byte, '02x') for Byte in newPacket])
                            self.CheckAndPrintNovii(bytearray.fromhex(pdata))    
                    newPacket = data[11:]
                else:
                    newPacket.extend(data[1:])
            except usb.core.USBError as e:
                sys.exit("Could not read from endpoint: %s" % str(e))

    def mycallback_MX(self):
        Label(self, text="SP02", padx=82, pady=20, relief=RIDGE, bg="MediumSeaGreen").grid(row=self._MX_rowCount,rowspan=2)
        # Old CRC
        old_crc = [0,0]
        newPacket = []
        cnt=0
        while True:
            try:
                data = self.ep_read_mx.read(self.ep_read_mx.wMaxPacketSize, timeout=100000)  #  40000000
                if data[1]==94 and data[2]==237:
                    if len(newPacket)!=0:
                        if newPacket[-2:]!=old_crc:
                            old_crc = newPacket[-2:]
                            pdata = ' '.join([format(Byte, '02x') for Byte in newPacket])
                            self.CheckAndPrintMX(bytearray.fromhex(pdata))    
                    newPacket = data[11:]
                else:
                    newPacket.extend(data[1:])
            except usb.core.USBError as e:
                sys.exit("Could not read from endpoint: %s" % str(e))        
              
    def mycallback_nsatx(self):
        Label(self, text="NSATX", padx=82, pady=20, relief=RIDGE, bg="MediumSeaGreen").grid(row=self._Nsatx_rowCount,rowspan=2)
        # Old CRC
        old_crc = [0,0]
        newPacket = []
        cnt=0
        while True:
            try:
                data = self._ep_read_nsatx.read(self._ep_read_nsatx.wMaxPacketSize, timeout=100000)
                if data[1]==94 and data[2]==237:
                    if len(newPacket)!=0:
                        if newPacket[-2:]!=old_crc:
                            old_crc = newPacket[-2:]
                            pdata = ' '.join([format(Byte, '02x') for Byte in newPacket])
                            self.CheckAndPrintNsatx(bytearray.fromhex(pdata))    
                    newPacket = data[11:]
                else:
                    newPacket.extend(data[1:])
            except usb.core.USBError as e:
                sys.exit("Could not read from endpoint: %s" % str(e))

        
   
    def mycallback_mecg(self):
        Label(self, text="MECG", padx=82, pady=20, relief=RIDGE, bg="MediumSeaGreen").grid(row=self._MECG_rowCount,rowspan=2)
        # Old CRC
        old_crc = [0,0]
        newPacket = []
        cnt=0
        while True:
            try:
                data = self._ep_read_mecg.read(self._ep_read_mecg.wMaxPacketSize, timeout=100000)
                if data[1]==94 and data[2]==237:
                    if len(newPacket)!=0:
                        if newPacket[-2:]!=old_crc:
                            old_crc = newPacket[-2:]
                            pdata = ' '.join([format(Byte, '02x') for Byte in newPacket])
                            self.CheckAndPrintMECG(bytearray.fromhex(pdata))    
                    newPacket = data[11:]
                else:
                    newPacket.extend(data[1:])
            except usb.core.USBError as e:
                sys.exit("Could not read from endpoint: %s" % str(e))

    def mycallback_iupc(self):
        
        Label(self, text="IUPC", padx=82, pady=20, relief=RIDGE, bg="MediumSeaGreen").grid(row=self._IUPC_rowCount,rowspan=2)
        # Old CRC
        old_crc = [0,0]
        newPacket = []
        cnt=0
        while True:
            try:
                data = self._ep_read_iupc.read(self._ep_read_iupc.wMaxPacketSize, timeout=100000)
                if data[1]==94 and data[2]==237:
                    if len(newPacket)!=0:
                        if newPacket[-2:]!=old_crc:
                            old_crc = newPacket[-2:]
                            pdata = ' '.join([format(Byte, '02x') for Byte in newPacket])
                            self.CheckAndPrintIUPC(bytearray.fromhex(pdata))    
                    newPacket = data[11:]
                else:
                    newPacket.extend(data[1:])
                #print ' '.join([format(Byte, '02x') for Byte in data]) 
                """
                new_crc = data[data[0]-1:]
                if new_crc!=old_crc:
                    old_crc = new_crc
                    print "Received new Data:"+ data
                        """
            except usb.core.USBError as e:
                sys.exit("Could not read from endpoint: %s" % str(e))

    def mycallback_fecg(self):
        Label(self, text="FECG", padx=82, pady=20, relief=RIDGE, bg="MediumSeaGreen").grid(row=self._FECG_rowCount,rowspan=2)
        # Old CRC
        old_crc = [0,0]
        newPacket = []
        cnt=0
        while True:
            try:
                data = self._ep_read_fecg.read(self._ep_read_fecg.wMaxPacketSize, timeout=100000)
                if data[1]==94 and data[2]==237:
                    if len(newPacket)!=0:
                        if newPacket[-2:]!=old_crc:
                            old_crc = newPacket[-2:]
                            pdata = ' '.join([format(Byte, '02x') for Byte in newPacket])
                            self.CheckAndPrintFECG(bytearray.fromhex(pdata))    
                    newPacket = data[11:]
                else:
                    newPacket.extend(data[1:])
                #print ' '.join([format(Byte, '02x') for Byte in data]) 
                """
                new_crc = data[data[0]-1:]
                if new_crc!=old_crc:
                    old_crc = new_crc
                    print "Received new Data:"+ data
                        """
            except usb.core.USBError as e:
                sys.exit("Could not read from endpoint: %s" % str(e))

    def mycallback_toco(self):
        Label(self, text="TOCO", padx=82, pady=20, relief=RIDGE, bg="MediumSeaGreen").grid(row=self._TOCO_rowCount,rowspan=2)
        # Old CRC
        old_crc = [0,0]
        newPacket = []
        cnt=0
        while True:
            try:
                data = self._ep_read_toco.read(self._ep_read_toco.wMaxPacketSize, timeout=100000)
                if data[1]==94 and data[2]==237:
                    if len(newPacket)!=0:
                        if newPacket[-2:]!=old_crc:
                            old_crc = newPacket[-2:]
                            pdata = ' '.join([format(Byte, '02x') for Byte in newPacket])
                            self.CheckAndPrintTOCO(bytearray.fromhex(pdata))    
                    newPacket = data[11:]
                else:
                    newPacket.extend(data[1:])
                #print ' '.join([format(Byte, '02x') for Byte in data]) 
                """
                new_crc = data[data[0]-1:]
                if new_crc!=old_crc:
                    old_crc = new_crc
                    print "Received new Data:"+ data
                        """
            except usb.core.USBError as e:
                sys.exit("Could not read from endpoint: %s" % str(e))

        

    def CheckAndPrint(self, bt):

        pi = ContentCounter()
        length = len(bt)
        while True:
            parent_hdr = struct.unpack(b'>HH', bt[pi.get():pi.forward(PARENT_HEADER_BYTES)])
            parent_id = parent_hdr[0]
            parent_length = parent_hdr[1]
            #print(parent_id, parent_length)
            parent_data = bt[pi.get():pi.forward(parent_length * WORD_BYTES)]
            #print(parent_data)
            ci = ContentCounter()
            while True:
                child_hdr = struct.unpack(b'>HH', parent_data[ci.get():ci.forward(CHILD_HEADER_BYTES)])
                child_id = child_hdr[0]
                child_length = child_hdr[1]
                if child_length > 0:
                    child_data = parent_data[ci.get():ci.forward(child_length * WORD_BYTES)]
                    #print "Child Tag #: ", '0x{0:04x}'.format(child_id) , 'Child Data #: ' ,' '.join(['{0:02x}'.format(ch) for ch in child_data])
                    if child_id not in datadict:
                        datadict[child_id] = child_data
                        local = ''.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varList[child_id] = StringVar()
                        self._varList[child_id].set(str(int(local,16)))
                        Label(self, text="Child Tag "+str(child_id), padx=32, pady=5,relief=RIDGE).grid(row=1, padx=5, column=self._columnCount)
                        Entry(self, textvariable=self._varList[child_id], justify=CENTER, state = "readonly",readonlybackground="white").grid(row=2, column=self._columnCount, padx=7, ipady=4)
                        self._columnCount += 1
                    elif datadict[child_id]!=child_data:
                        datadict[child_id] = child_data
                        local = ''.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varList[child_id].set(str(int(local,16)))
                if ci.get() > len(parent_data) - CHILD_HEADER_BYTES:
                    break
            if pi.get() >= length - PARENT_HEADER_BYTES:
                return             


    def CheckAndPrintNovii(self, bt):
        pi = ContentCounter()
        length = len(bt)
        while True:
            parent_hdr = struct.unpack(b'>HH', bt[pi.get():pi.forward(PARENT_HEADER_BYTES)])
            parent_id = parent_hdr[0]
            parent_length = parent_hdr[1]
            #print(parent_id, parent_length)
            parent_data = bt[pi.get():pi.forward(parent_length * WORD_BYTES)]
            #print(parent_data)
            ci = ContentCounter()
            while True:
                child_hdr = struct.unpack(b'>HH', parent_data[ci.get():ci.forward(CHILD_HEADER_BYTES)])
                child_id = child_hdr[0]
                child_length = child_hdr[1]
                if child_length > 0:
                    child_data = parent_data[ci.get():ci.forward(child_length * WORD_BYTES)]
                    #print "Child Tag #: ", '0x{0:04x}'.format(child_id) , 'Child Data #: ' ,' '.join(['{0:02x}'.format(ch) for ch in child_data])
                    if child_id not in datadictNovii[parent_id%10]:
                        datadictNovii[parent_id%10][child_id] = child_data
                        local = ' '.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varListNovii[parent_id%10][child_id] = StringVar()
                        self._varListNovii[parent_id%10][child_id].set(local)
                        Label(self, text="Child Tag "+str(child_id), padx=32, pady=5,relief=RIDGE).grid(row=self._rowCount, padx=5, column=self._Novii_columnCount)
                        Entry(self, textvariable=self._varListNovii[parent_id%10][child_id], justify=CENTER, state = "readonly",readonlybackground="white").grid(row=self._rowCount+1, column=self._Novii_columnCount, padx=7, ipady=4)
                        self._Novii_columnCount += 1
                        if (self._Novii_columnCount == 8):
                            self._rowCount += 2
                            self._Novii_columnCount = 1
                        #print "Child Tag #: ", '0x{0:04x}'.format(child_id) , 'Child Data #: ' ,' '.join(['{0:02x}'.format(ch) for ch in child_data])
                    elif datadictNovii[parent_id%10][child_id]!=child_data:
                        datadictNovii[parent_id%10][child_id] = child_data
                        local = ' '.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varListNovii[parent_id%10][child_id].set(local)
                        #print "Child Tag #: ", '0x{0:04x}'.format(child_id) , 'Child Data #: ' ,' '.join(['{0:02x}'.format(ch) for ch in child_data])
                if ci.get() > len(parent_data) - CHILD_HEADER_BYTES:
                    break
            if pi.get() >= length - PARENT_HEADER_BYTES:
                return
            
    def CheckAndPrintMX(self, bt):
        pi = ContentCounter()
        length = len(bt)
        while True:
            parent_hdr = struct.unpack(b'>HH', bt[pi.get():pi.forward(PARENT_HEADER_BYTES)])
            parent_id = parent_hdr[0]
            parent_length = parent_hdr[1]
            #print(parent_id, parent_length)
            parent_data = bt[pi.get():pi.forward(parent_length * WORD_BYTES)]
            #print(parent_data)
            ci = ContentCounter()
            while True:
                child_hdr = struct.unpack(b'>HH', parent_data[ci.get():ci.forward(CHILD_HEADER_BYTES)])
                child_id = child_hdr[0]
                child_length = child_hdr[1]
                if child_length > 0:
                    child_data = parent_data[ci.get():ci.forward(child_length * WORD_BYTES)]
                    if child_id not in datadictMX:
                        datadictMX[child_id] = child_data
                        local = ' '.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varListMX[child_id] = StringVar()
                        self._varListMX[child_id].set(local)
                        Label(self, text="Child Tag "+str(child_id), padx=32, pady=5,relief=RIDGE).grid(row=self._MX_rowCount, padx=5, column=self._MX_columnCount)
                        Entry(self, textvariable=self._varListMX[child_id], justify=CENTER, state = "readonly",readonlybackground="white").grid(row=self._MX_rowCount+1, column=self._MX_columnCount, padx=7, ipady=4)
                        self._MX_columnCount += 1
                        if (self._MX_columnCount == 8):
                            self._MX_rowCount += 2
                            self._MX_columnCount = 1
                    elif datadictMX[child_id]!=child_data:
                        datadictMX[child_id] = child_data
                        local = ' '.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varListMX[child_id].set(local)
                if ci.get() > len(parent_data) - CHILD_HEADER_BYTES:
                    break
            if pi.get() >= length - PARENT_HEADER_BYTES:
                return 

    def CheckAndPrintNsatx(self, bt):
        pi = ContentCounter()
        length = len(bt)
        while True:
            parent_hdr = struct.unpack(b'>HH', bt[pi.get():pi.forward(PARENT_HEADER_BYTES)])
            parent_id = parent_hdr[0]
            parent_length = parent_hdr[1]
            #print(parent_id, parent_length)
            parent_data = bt[pi.get():pi.forward(parent_length * WORD_BYTES)]
            #print(parent_data)
            ci = ContentCounter()
            while True:
                child_hdr = struct.unpack(b'>HH', parent_data[ci.get():ci.forward(CHILD_HEADER_BYTES)])
                child_id = child_hdr[0]
                child_length = child_hdr[1]
                if child_length > 0:
                    child_data = parent_data[ci.get():ci.forward(child_length * WORD_BYTES)]
                    #print "Child Tag #: ", '0x{0:04x}'.format(child_id) , 'Child Data #: ' ,' '.join(['{0:02x}'.format(ch) for ch in child_data])
                    if child_id not in datadictNsatx:
                        datadictNsatx[child_id] = child_data
                        local = ' '.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varListNsatx[child_id] = StringVar()
                        self._varListNsatx[child_id].set(local)
                        Label(self, text="Child Tag "+str(child_id), padx=32, pady=5,relief=RIDGE).grid(row=self._Nsatx_rowCount, padx=5, column=self._Nsatx_columnCount)
                        Entry(self, textvariable=self._varListNsatx[child_id], justify=CENTER, state = "readonly",readonlybackground="white").grid(row=self._Nsatx_rowCount+1, column=self._Nsatx_columnCount, padx=7, ipady=4)
                        self._Nsatx_columnCount += 1
                        if (self._Nsatx_columnCount == 8):
                            self._Nsatx_rowCount += 2
                            self._Nsatx_columnCount = 1
                    elif datadictNsatx[child_id]!=child_data:
                        datadictNsatx[child_id] = child_data
                        local = ' '.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varListNsatx[child_id].set(local)
                if ci.get() > len(parent_data) - CHILD_HEADER_BYTES:
                    break
            if pi.get() >= length - PARENT_HEADER_BYTES:
                return
            
        
    def CheckAndPrintMECG(self, bt):
        pi = ContentCounter()
        length = len(bt)
        while True:
            parent_hdr = struct.unpack(b'>HH', bt[pi.get():pi.forward(PARENT_HEADER_BYTES)])
            parent_id = parent_hdr[0]
            parent_length = parent_hdr[1]
            #print(parent_id, parent_length)
            parent_data = bt[pi.get():pi.forward(parent_length * WORD_BYTES)]
            #print(parent_data)
            ci = ContentCounter()
            while True:
                child_hdr = struct.unpack(b'>HH', parent_data[ci.get():ci.forward(CHILD_HEADER_BYTES)])
                child_id = child_hdr[0]
                child_length = child_hdr[1]
                if child_length > 0:
                    child_data = parent_data[ci.get():ci.forward(child_length * WORD_BYTES)]
                    #print "Child Tag #: ", '0x{0:04x}'.format(child_id) , 'Child Data #: ' ,' '.join(['{0:02x}'.format(ch) for ch in child_data])
                    if child_id not in datadictMECG[parent_id]:
                        datadictMECG[parent_id][child_id] = child_data
                        local = ' '.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varListMECG[parent_id][child_id] = StringVar()
                        self._varListMECG[parent_id][child_id].set(local)
                        Label(self, text=str(parent_id)+" "+str(child_id), padx=32, pady=5,relief=RIDGE).grid(row=self._MECG_rowCount, padx=5, column=self._MECG_columnCount)
                        Entry(self, textvariable=self._varListMECG[parent_id][child_id], justify=CENTER, state = "readonly",readonlybackground="white").grid(row=self._MECG_rowCount+1, column=self._MECG_columnCount, padx=7, ipady=4)
                        self._MECG_columnCount += 1
                        if (self._MECG_columnCount == 8):
                            self._MECG_rowCount += 2
                            self._MECG_columnCount = 1
                    elif datadictMECG[parent_id][child_id]!=child_data:
                        datadictMECG[parent_id][child_id] = child_data
                        local = ' '.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varListMECG[parent_id][child_id].set(local)
                if ci.get() > len(parent_data) - CHILD_HEADER_BYTES:
                    break
            if pi.get() >= length - PARENT_HEADER_BYTES:
                return
    

    def CheckAndPrintIUPC(self, bt):
        pi = ContentCounter()
        length = len(bt)
        while True:
            parent_hdr = struct.unpack(b'>HH', bt[pi.get():pi.forward(PARENT_HEADER_BYTES)])
            parent_id = parent_hdr[0]
            parent_length = parent_hdr[1]
            #print(parent_id, parent_length)
            parent_data = bt[pi.get():pi.forward(parent_length * WORD_BYTES)]
            #print(parent_data)
            ci = ContentCounter()
            while True:
                child_hdr = struct.unpack(b'>HH', parent_data[ci.get():ci.forward(CHILD_HEADER_BYTES)])
                child_id = child_hdr[0]
                child_length = child_hdr[1]
                if child_length > 0:
                    child_data = parent_data[ci.get():ci.forward(child_length * WORD_BYTES)]
                    #print "Child Tag #: ", '0x{0:04x}'.format(child_id) , 'Child Data #: ' ,' '.join(['{0:02x}'.format(ch) for ch in child_data])
                    if child_id not in datadictIUPC:
                        datadictIUPC[child_id] = child_data
                        local = ' '.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varListIUPC[child_id] = StringVar()
                        self._varListIUPC[child_id].set(local)
                        Label(self, text="Child Tag "+str(child_id), padx=32, pady=5,relief=RIDGE).grid(row=self._IUPC_rowCount, padx=5, column=self._IUPC_columnCount)
                        Entry(self, textvariable=self._varListIUPC[child_id], justify=CENTER, state = "readonly",readonlybackground="white").grid(row=self._IUPC_rowCount+1, column=self._IUPC_columnCount, padx=7, ipady=4)
                        self._IUPC_columnCount += 1
                        if (self._IUPC_columnCount == 8):
                            self._IUPC_rowCount += 2
                            self._IUPC_columnCount = 1
                    elif datadictIUPC[child_id]!=child_data:
                        datadictIUPC[child_id] = child_data
                        local = ' '.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varListIUPC[child_id].set(local)
                if ci.get() > len(parent_data) - CHILD_HEADER_BYTES:
                    break
            if pi.get() >= length - PARENT_HEADER_BYTES:
                return

    def CheckAndPrintFECG(self, bt):
        pi = ContentCounter()
        length = len(bt)
        while True:
            parent_hdr = struct.unpack(b'>HH', bt[pi.get():pi.forward(PARENT_HEADER_BYTES)])
            parent_id = parent_hdr[0]
            parent_length = parent_hdr[1]
            #print(parent_id, parent_length)
            parent_data = bt[pi.get():pi.forward(parent_length * WORD_BYTES)]
            #print(parent_data)
            ci = ContentCounter()
            while True:
                child_hdr = struct.unpack(b'>HH', parent_data[ci.get():ci.forward(CHILD_HEADER_BYTES)])
                child_id = child_hdr[0]
                child_length = child_hdr[1]
                if child_length > 0:
                    child_data = parent_data[ci.get():ci.forward(child_length * WORD_BYTES)]
                    #print "Child Tag #: ", '0x{0:04x}'.format(child_id) , 'Child Data #: ' ,' '.join(['{0:02x}'.format(ch) for ch in child_data])
                    if child_id not in datadictFECG:
                        datadictFECG[child_id] = child_data
                        local = ' '.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varListFECG[child_id] = StringVar()
                        self._varListFECG[child_id].set(local)
                        Label(self, text="Child Tag "+str(child_id), padx=32, pady=5,relief=RIDGE).grid(row=self._FECG_rowCount, padx=5, column=self._FECG_columnCount)
                        Entry(self, textvariable=self._varListFECG[child_id], justify=CENTER, state = "readonly",readonlybackground="white").grid(row=self._FECG_rowCount+1, column=self._FECG_columnCount, padx=7, ipady=4)
                        self._FECG_columnCount += 1
                        if (self._FECG_columnCount == 8):
                            self._FECG_rowCount += 2
                            self._FECG_columnCount = 1
                    elif datadictFECG[child_id]!=child_data:
                        datadictFECG[child_id] = child_data
                        local = ' '.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varListFECG[child_id].set(local)
                if ci.get() > len(parent_data) - CHILD_HEADER_BYTES:
                    break
            if pi.get() >= length - PARENT_HEADER_BYTES:
                return

    def CheckAndPrintTOCO(self, bt):
        pi = ContentCounter()
        length = len(bt)
        while True:
            parent_hdr = struct.unpack(b'>HH', bt[pi.get():pi.forward(PARENT_HEADER_BYTES)])
            parent_id = parent_hdr[0]
            parent_length = parent_hdr[1]
            #print(parent_id, parent_length)
            parent_data = bt[pi.get():pi.forward(parent_length * WORD_BYTES)]
            #print(parent_data)
            ci = ContentCounter()
            while True:
                child_hdr = struct.unpack(b'>HH', parent_data[ci.get():ci.forward(CHILD_HEADER_BYTES)])
                child_id = child_hdr[0]
                child_length = child_hdr[1]
                if child_length > 0:
                    child_data = parent_data[ci.get():ci.forward(child_length * WORD_BYTES)]
                    #print "Child Tag #: ", '0x{0:04x}'.format(child_id) , 'Child Data #: ' ,' '.join(['{0:02x}'.format(ch) for ch in child_data])
                    if child_id not in datadictTOCO:
                        datadictTOCO[child_id] = child_data
                        local = ' '.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varListTOCO[child_id] = StringVar()
                        self._varListTOCO[child_id].set(local)
                        Label(self, text="Child Tag "+str(child_id), padx=32, pady=5,relief=RIDGE).grid(row=self._TOCO_rowCount, padx=5, column=self._TOCO_columnCount)
                        Entry(self, textvariable=self._varListTOCO[child_id], justify=CENTER, state = "readonly",readonlybackground="white").grid(row=self._TOCO_rowCount+1, column=self._TOCO_columnCount, padx=7, ipady=4)
                        self._TOCO_columnCount += 1
                        if (self._TOCO_columnCount == 8):
                            self._TOCO_rowCount += 2
                            self._TOCO_columnCount = 1
                    elif datadictTOCO[child_id]!=child_data:
                        datadictTOCO[child_id] = child_data
                        local = ' '.join(['{0:02x}'.format(ch) for ch in child_data])
                        self._varListTOCO[child_id].set(local)
                if ci.get() > len(parent_data) - CHILD_HEADER_BYTES:
                    break
            if pi.get() >= length - PARENT_HEADER_BYTES:
                return
        


root = Tk()
#root.geometry('600x700+200+100')
scrollbar = AutoScrollbar(root)
scrollbar.grid(row=0, column=1, sticky=N+S)
canv = Canvas(root, relief=SUNKEN)
canv.grid(row=0, column=0, sticky=N+S+E+W)
scrollbar.config(command = canv.yview)
canv.config(yscrollcommand=scrollbar.set)
# make the canvas expandable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
frame = Frame(canv)
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
App = Acs_Test_App(frame)
App.start_transaction()
time.sleep(2)
root.update()
#frame.update_idletasks()
canv.create_window(3100, 3100, anchor=NW, window=frame)
canv.config(scrollregion=canv.bbox("all"))

root.mainloop()




Content_Counter.py
class ContentCounter(object):

    def __init__(self):
        self._index = 0

    def get(self):
        return self._index

    def forward(self, steps):
        self._index += steps
        return self._index
