#!/usr/bin/python3

import serial

from extract_value import extract_str
from sent_to_google_sheet import sent_data

def main():
    """Logging PLC data

    Write data to file data.txt
    """
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
        receive = str(port.read())
        buffer_read += receive
        if receive == "*":
            with open("log.txt", "a") as file_out:
                file_out.write(buffer_read)
            value = extract_str(buffer_read)
            if value:
                print("Sent to server", value)
            buffer_read = "" 



if __name__ == '__main__':
    main()

