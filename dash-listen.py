#Import config file 
import config

import socket
import struct
import binascii
import time
from subprocess import call
import os, pwd

#This makes the button pause spotify and do a little sound

#Some info: https://familab.org/2016/02/hacking-the-amazon-dash-button-to-make-a-simple-cheap-iot-place-anywhere-networked-button-3/



rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0806))

lastExecute = 0

while True:

    packet = rawSocket.recvfrom(2048)

    ethernet_header = packet[0][0:14]
    ethernet_detailed = struct.unpack("!6s6s2s", ethernet_header)

    arp_header = packet[0][14:42]
    arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header)

    source_mac = binascii.hexlify(arp_detailed[5])
    dest_ip = socket.inet_ntoa(arp_detailed[8])
    if (source_mac == config.mac):
        print "Button Pressed - IP = " + dest_ip
        if int(time.time()) > (lastExecute + (5)):
            lastExecute = int(time.time())

            #command = "dbus-send --system --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause"
            command = "./pspot"
            print("pausing spotify")
            uid = pwd.getpwnam(config.uid)[2] #instead of index 2 you can use pw_uid Attribute
            print("UID: " + str(uid))
            os.setuid(uid)
            os.system(command)

            time.sleep(1)
            call(["mpg123", config.soundfile])

