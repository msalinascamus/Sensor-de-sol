import rospy
import serial
from threading import Thread
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray
from btsensor import btReceiver
from std_msgs.msg import UInt8
import numpy as np
import math
import csv
import datetime as dt 
import codecs 
import cStringIO

class MagInterface:
    def __init__(self):
        # Only argument stuff
        self.running = False
        self.bt_receiver = btReceiver(debug = True)
        self.data = {}
        self.data_values = []
        self.counter = 0

    def initialize(self):
        # Get params and allocate msgs
        self.state_update_rate = rospy.get_param('/rate', 50)
        self.bt_receiver.initialize()

    def start(self):
        # Create subs, services, publishers, threads
        self.running = True
        #publishers
        self.data1_pub = rospy.Publisher('/voltaje', Float32, queue_size=70)
        self.data2_pub = rospy.Publisher('/angulo', Float32, queue_size=70)
        self.data4_pub = rospy.Publisher('/checksum', UInt8, queue_size=70)
        Thread(target=self.update_state).start()

    def stop(self):
        self.running = False

        self.data1_pub.unregister()
        self.data2_pub.unregister()
        self.data4_pub.unregister()

    def update_state(self):
        rate = rospy.Rate(self.state_update_rate)
        while self.running and not rospy.is_shutdown():
            if(self.bt_receiver.read()):
                packet = self.bt_receiver.packet
                voltaje = packet[0]
                checksum = packet[1]
                if voltaje <= 0.2:
                    angulo = 90
                else:
                    angulo = math.degrees(np.arccos(voltaje/5))
                self.data1_pub.publish(float(voltaje))
                self.data2_pub.publish(float(angulo))
                self.data4_pub.publish(UInt8(checksum))
                self.getdata()
                #except: 
                 #   print ("incomplete data")
                rate.sleep()
                           
    def getdata(self):
        packet = self.bt_receiver.packet
        data_voltaje = packet[0]
        if data_voltaje <= 0.2:
            data_angulo = 90
        else:
            data_angulo = math.degrees(np.arccos(data_voltaje/5))
        #data_tiempo = dt.datetime.now().strftime('%H:%M:%S.%f')
        self.counter =+ 1
        self.data_values.append(str(data_voltaje)) 
        self.data_values.append(str(data_angulo))
        self.data.update({self.counter: self.data_values})
        self.data_values = []
        print self.data

    def savedata(self):
        with open('/home/mariana/Escritorio/spel/ADCS/Python/Sensor/datos.csv', 'a') as outfile:
            writer = csv.writer(outfile)
            #header = {"Tiempo": ["Voltaje", "Angulo"]}
            #for key, value in header.items():
            #    v = value[0]
            #    a = value[1]
            #    writer.writerow([key, v,a])
            for key, value in self.data.items():
                v = value[0]
                a = value[1]
                writer.writerow([key, v, a])
                
           

if __name__ == '__main__':
    rospy.init_node('ros_bt_interface')
    mg_ros = MagInterface()
    mg_ros.initialize()
    mg_ros.start()
    rospy.spin()
    mg_ros.savedata()
    mg_ros.stop()
