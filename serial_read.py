#!/usr/bin/python3

import serial
import struct
import datetime
from time import sleep

from extract_value import extract_str
from sent_to_google_sheet import sent_data

def local_log(fins):
    '''Append fins data to log file
    '''
    print(fins)
    with open("log.txt", "a") as file_out:
        file_out.write(fins)

def server_log(log_variable):
    #local backup
    with open("sent.txt", "a") as file_out:
        file_out.write(str(log_variable) + "\n")
    #server log
    sent_data([log_variable])

def main():
    '''Logging PLC data

    Write data to file data.txt
    '''
    #serial read variable
    port = None
    buffer_read = ""

    #log variable
    rfid = "dummy"
    start = ""
    end = ""
    max_load = ""
    status = ""
    
    #try connecting to port
    while port is None:
        try:
            port = serial.Serial(
                port = '/dev/ttyUSB0',
                baudrate = 9600,
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS,
                timeout = 1,
                rtscts = False,
                dsrdtr = False,
                xonxoff = False)
        except Exception:
            print("USB not found")
            sleep(1)

    #start logging forever
    while True:
        receive = port.read()
        receive_decode = ""

        #decode bytes
        try:
            receive_decode = receive.decode()
            buffer_read += str(receive_decode)
        except ValueError:
            #ignore
            pass

        if receive_decode == "*":
            local_log(buffer_read)

            data_list = extract_str(buffer_read.replace("\n", "")
                .replace("\r", ""))

            #check if data_list not empty
            if data_list:
                address = data_list[1]
                value = data_list[3]
                if address == "015F00": #start time
                    start = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
                elif address == "016000": #end time
                    end = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
                elif address == "016300": #status passed
                    status = "PASSED"
                elif address == "016400": #status sot passed
                    status = "NOT PASSED"
                elif address == "015E00": #max load
                    max_load = struct.unpack('!f', 
                        bytes.fromhex(value[4:8] + value[0:4]))[0]

                    server_log([rfid, start, end, max_load, status])

                    #reset log variable
                    rfid = "dummy"
                    start = ""
                    end = ""
                    max_load = ""
                    status = ""

            #reset buffer
            buffer_read = "" 


if __name__ == '__main__':
    main()

