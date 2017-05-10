#!/usr/bin/python3

import struct
import datetime
import os
import signal
import subprocess
from time import sleep

from fins import extract_str
from serial_helper import connect_port

#Testing device code
DEVICE = "TORSI"

def local_log(fins):
    '''Append all fins communication to log file
    '''
    print(fins)
    with open("hmi_fins.txt", "a") as file_out:
        file_out.write(fins)

def server_log(testing_result):
    '''Sent testing result to server
    '''
    #local backup
    with open("hmi_sent.txt", "a") as file_out:
        file_out.write(str(testing_result) + "\n")
    #server log
    #TODO: Remove google sheet log, upload  to server.
    
def dir_log(testing_result):
    '''Save testing result to directory
    '''
    vendor = "VENDOR"
    category = "CATEGORY"
    product = testing_result[1]
    with open("product.txt", "r") as f:
        for line in f:
            data = line.split(",")
            if data[0] == product:
                vendor = data[2].replace("\n", "")
                category = data[1]
                break
    
    folder = vendor + "_" + category + "_" + product + "_" + DEVICE
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)
    
    with open(folder + ".csv", "w") as f:
        f.write(",".join(str(x) for x in testing_result))
        f.write("\n")
    os.chdir("..")

def logging():
    '''Logging PLC data

    Write data to file data.txt
    '''
    
    #product
    with open("product_tmp.txt", "r") as f:
        for line in f:
            product = line
    
    #product
    with open("tester_tmp.txt", "r") as f:
        for line in f:
            tester = line
            
    #remove temporal data
    #os.remove("tester_tmp.txt")
    #os.remove("product_tmp.txt")
            
    print("Testing product: ", product)
    #serial read buffer
    buff = ""

    #hmi data
    start = ""
    end = ""
    max_load_cw = ""
    max_load_ccw = ""
            
    #connect to port
    ser = connect_port("/dev/ttyUSB0")

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
            local_log(buff)

            data_list = extract_str(buff.replace("\n", "")
                .replace("\r", ""))

            #check if data_list not empty
            if data_list:
                address = data_list[1]
                value = data_list[3]
                if address == "016900": #start time
                    start = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
                    with open("rfid_pid.txt") as f:
                        pid = f.readline()
                        #os.kill(int(pid), signal.SIGKILL)
                elif address == "016A00": #end time
                    end = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
                elif address == "016B00": #status passed
                    status = "PASSED"
                elif address == "016C00": #status sot passed
                    status = "NOT PASSED"
                elif address == "015E00": #max load
                    max_load_cw = struct.unpack('!f', 
                        bytes.fromhex(value[4:8] + value[0:4]))[0]
                    max_load_ccw = struct.unpack('!f',
                        bytes.fromhex(value[12:16] + value[8:12]))[0]
                                            
                    #server_log([tester, product,start, end, max_load, status])
                    dir_log([tester, product, start, end, max_load_cw, max_load_ccw, status])
                    
                    #finish
                    subprocess.call([
                        "lxterminal", 
                        "-e", 
                        "python3 /home/pi/RasberryPI/main_program.py"
                    ])
                    exit(0)

            #reset buffer
            buff = "" 
            
if __name__ == "__main__":
    logging()
