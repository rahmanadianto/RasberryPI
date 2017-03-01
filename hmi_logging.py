import struct
import datetime
from time import sleep

from fins import extract_str
from google_sheet_api import sent_data
from serial_helper import connect_port

def local_log(fins):
    '''Append all fins communication to log file
    '''
    print(fins)
    with open("hmi_fins.txt", "a") as file_out:
        file_out.write(fins)

def server_log(log_variable):
    '''Sent extracted value to server
    '''
    #local backup
    with open("hmi_sent.txt", "a") as file_out:
        file_out.write(str(log_variable) + "\n")
    #server log
    sent_data([log_variable])

def logging():
    '''Logging PLC data

    Write data to file data.txt
    '''
    #serial read buffer
    buff = ""

    #hmi data
    start = ""
    end = ""
    max_load = ""
    status = ""

    #other data
    rfid = "dummy"
    
    #connect to port
    ser = connect_port("/dev/ttyUSB0")

    #start logging forever
    while True:
        receive = port.read()
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

            #check if hmi data has completed
            if start and end and max_load and status:
                server_log([rfid, start, end, max_load, status])

                #reset hmi data
                start = ""
                end = ""
                max_load = ""
                status = ""

            #reset buffer
            buff = "" 
