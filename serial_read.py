#!/usr/bin/python3

import serial

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
        receive = port.read()
        print(receive)
        file_out.write(str(receive))