#!/usr/bin/python3

import serial

from extract_value import extract_str
from sent_to_google_sheet import sent_data

def local_log(fins):
    '''Append fins data to log file
    '''
    with open("log.txt", "a") as file_out:
        file_out.write(fins)

def server_log(value):
    print("Sent:", value)

def main():
    '''Logging PLC data

    Write data to file data.txt
    '''
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

    buffer_read = ""

    while True:
        receive = port.read()
        receive_decode = ""

        #decode bytes
        if isinstance(receive, bytes):
            receive_decode = receive.decode()
            buffer_read += receive_decode
        else:
            receive_decode = ""

        if receive_decode == "*":
            local_log(buffer_read)

            value = extract_str(buffer_read.replace("\n", "").replace("\r", ""))
            #check if value not empty
            if value: 
                server_log()

            buffer_read = "" 



if __name__ == '__main__':
    main()

