import serial
from time import sleep

def connect_port(port):
    ser = None
    while ser is None:
        try:
            ser = serial.Serial(
                port = port,
                baudrate = 9600,
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS,
                timeout = 1,
                rtscts = False,
                dsrdtr = False,
                xonxoff = False)
        except Exception:
            print("Connecting failed, try again in 3 seconds")
            sleep(3)

    return ser
