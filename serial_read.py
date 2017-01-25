#!/usr/bin/python3

import serial

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
        writeTimeout = 0,
        timeout = 1,
        rtscts = False,
        dsrdtr = False,
        xonxoff = False)

    while True:
        with open("data.txt", "a") as file_out:
            #Receive one character
            receive = port.read()
            print(receive)
            #Append character to file
            file_out.write(str(receive))



if __name__ == '__main__':
    main()

