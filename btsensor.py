__author__ = 'gdiaz'

import time
import bluetooth
from threading import Timer
import struct
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.animation as animation

class btReceiver(object):
    def __init__(self, debug = False):
        self.btSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)        
        self.packet = [0,0,0,0,0,0]
        self.debug = debug
        self.time = []

    def initialize(self):
        #Buetooth
        # bt_addr = "00:13:04:03:00:02" #CUBE
        bt_addr = "30:14:11:10:08:12" #SATBOT(one axis)
        local_port = 1
        # TO DO: check if actually succeed
        self.btSocket.connect((bt_addr, local_port))
        # self.btSocket.connect(("00:13:04:03:00:02", 1))
        print( "Conection succed! starting comunication ...")

    def stop(self):
        print( "Conection Finish. Closing ports ...")
        self.btSocket.close()

    def reset(self):
        self.packet = [0,0,0,0,0,0]

    def DEBUG_PRINT(self, msg_type, msg):
        if not(self.debug): return
        if msg_type == "info":
            print( chr(27)+"[0;32m"+"[INFO]: "+chr(27)+"[0m" + msg)
        elif msg_type == "warn":
            print( chr(27)+"[0;33m"+"[WARN]: "+chr(27)+"[0m" + msg)
        elif msg_type == "error":
            print( chr(27)+"[0;31m"+"[ERROR]: "+chr(27)+"[0m" + msg)
        elif msg_type == "alert":
            print( chr(27)+"[0;34m"+"[ALERT]: "+chr(27)+"[0m" + msg)
        else:
            print( "NON implemented Debug print type")

    def checksum(self, packet, sz):
        sum = 0
        for j in range(0,sz-1): sum += packet[j]
        return sum

    def read(self):
        i = 0
        k = 0
        sz = 5
        maximo = 5 #voltaje maximo del sensor
        self.reset()
        while (k < 2*sz):
            byte = self.btSocket.recv(1)
            self.packet[i] = ord(byte)
            i+=1
            if (i==sz):
                print(self.packet)
                chksm = self.checksum(self.packet, sz) & 0x00FF #Low byte of data checksum
                if (chksm == self.packet[sz-1] and chksm !=0):
                    self.DEBUG_PRINT("info", "frame received = "+str(self.packet))
                    p = struct.pack('BBBBB', self.packet[0],self.packet[1],self.packet[2],self.packet[3],self.packet[4])
                    self.packet = struct.unpack("fB", p)
                    #print self.packet
                    return True
                else:
                    for j in range(0,sz-1): self.packet[j] = self.packet[j+1] #Shift Left packet
                    self.packet[sz-1] = 0 #Clean last byte to receive other packet
                    i = sz-1
                    self.DEBUG_PRINT("warn", "Bad checksum = "+str(chksm))
            k+=1
        # Packet not received Correctly
        self.DEBUG_PRINT("error", "Frame lost")
        self.reset()
        # for j in range(0,sz): self.packet[j] = 0 #Reset packet
        return False
        #try:
         #   print struct.unpack("fffi", byte)
        #except:
         #   pass

if __name__ == '__main__':
    bt_receiver = btReceiver(debug = True)
    bt_receiver.initialize()    
    # test read
    while True:
        bt_receiver.read()   
    bt_receiver.stop()

