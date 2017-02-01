#!/usr/bin/python3

import serial
import struct

from extract_value import extract_str
from sent_to_google_sheet import sent_data

def local_log(fins):
    '''Append fins data to log file
    '''
    print(fins)
    with open("log.txt", "a") as file_out:
        file_out.write(fins)

def server_log(value):
    print("Sent:", value)
    with open("sent.txt", "a") as file_out:
        file_out.write(str(value) + "\n")
        
    rfid = "NONE"
    start = "NONE"
    end = "NONE"
    data = struct.unpack('!f', bytes.fromhex(value[3][4:8] + value[3][0:4]))[0]
    status = "NOT PASSED"
    sent_data([[rfid, start, end, data, status]])

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
        try:
            receive_decode = receive.decode()
            buffer_read += str(receive_decode)
        except ValueError:
            #ignore
            pass

        if receive_decode == "*":
            local_log(buffer_read)

            value = extract_str(buffer_read.replace("\n", "").replace("\r", ""))
            #check if value not empty
            if value and value[1] == '015E00':
                server_log(value)

            #reset buffer
            buffer_read = "" 


if __name__ == '__main__':
    main()

