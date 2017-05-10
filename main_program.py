#!/usr/bin/python3

import struct
import datetime
import os
import subprocess
from time import sleep

from fins import extract_str
from serial_helper import connect_port
from server import download_data

def main():
    '''Main Program
    
    Handle welcom screen
    '''
    print("Starting app..")

    #serial read buffer
    buff = ""
    
    #connect to port
    ser = connect_port("/dev/ttyUSB0")
    
    print("App ready")

    #start logging forever
    while True:
        receive = ser.read()
        receive_decode = ""

        #decode bytes
        try:
            receive_decode = receive.decode()
            buff += str(receive_decode)
        except ValueError:
            #ignore
            pass

        if receive_decode == "*":
            print(buff)
            data_list = extract_str(buff.replace("\n", "")
                .replace("\r", ""))

            #check if data_list not empty
            if data_list:
                address = data_list[1]
                if address == "016800" or address == "015F00": #start read rfid
                    #download_data()
                    subprocess.call([
                        "lxterminal", 
                        "-e", 
                        "python3 /home/pi/RasberryPI/rfid_v2.py"
                    ])
                    exit(0)

            #reset buffer
            buff = "" 
    
if __name__ == "__main__":
    main()

