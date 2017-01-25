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
        baudrate = 19200,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 10,
        rtscts = False,
        dsrdtr = False,
        xonxoff = False)

    while True:
        with open("log.txt", "a") as file_out:
            #receive byte until eol or timeout
            receive = str(port.readline())
            file_out.write(receive)

            value = extract_str(receive)
            if value:
                print(value) 



if __name__ == '__main__':
    main()

