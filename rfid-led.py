from time import sleep
from subprocess import call

from serial_helper import connect_port
from hmi_logging import logging
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)        
GPIO.setwarnings(False)
GPIO.setup(11,GPIO.OUT)
 
def init_rfid(ser):
    '''Sent initialization command bytes to rfid
    '''
    print("Connecting rfid...")
    ser.write(b"\xfe")
    sleep(0.2)
    ser.write(b"\xfe")
    sleep(0.2)
    ser.write(b"\xe1")
    sleep(0.2)
    ser.write(b"\xc2")
    ser.write(b"\xff")
    sleep(0.2)
    ser.write(b"\x20")
    ser.write(b"\xc0")
    sleep(0.2)
    ser.write(b"\x40")
    ser.write(b"\x02")
    ser.write(b"\x02")
    ser.write(b"\xbc")
    ser.write(b"\x40")
    ser.write(b"\x02")
    ser.write(b"\x02")
    ser.write(b"\xbc")
    sleep(1)
    ser.write(b"\x40")
    ser.write(b"\x02")
    ser.write(b"\x06")
    ser.write(b"\xb8")
    sleep(1)
    ser.write(b"\x40")
    ser.write(b"\x03")
    ser.write(b"\x0a")
    ser.write(b"\x01")
    ser.write(b"\xb2")
    sleep(1)

def sent_read_cmd(ser):
    '''Sent read command to rfid, request data from rfid
    '''
    ser.write(b"\x40")
    ser.write(b"\x06")
    ser.write(b"\xee")
    ser.write(b"\x01")
    ser.write(b"\x00")
    ser.write(b"\x00")
    ser.write(b"\x00")
    ser.write(b"\xcb")
    ser.write(b"\x40")
    ser.write(b"\x06")
    
def save_rfid(data):
    with open("tmp.txt", "w") as f:
        f.write(data)

def read_rfid():
    '''Listening to rfid
    '''
    ser = connect_port("/dev/ttyS0")
    buff = ""
    buff_list = []
    first = True

    init_rfid(ser)
        
    while True: 
         
        read = True;
        print("Waiting rfid data...")
     
        while read:
             
            receive = ser.read()
            str_log = ""
            
            try:
                str_log = str(hex(ord(receive)))
                
                if str_log == "0xee":
                    
                    if len(buff_list) > 5:
                        rfid = buff_list[3:len(buff_list)-3]
                        rfid_str = ""
                        for x in rfid:
                            xv= x.replace("0x", "")
                            if len(xv) < 2:
                                xv = "0" + xv
                            rfid_str += xv
                        if not first:
                            print(rfid_str)
                            save_rfid(rfid_str)
                            sleep(1)
                            call(["lxterminal", "-e", "python3 /home/pi/RasberryPI/hmi_logging.py"])
                            exit(0)
                        first = False
                    
                    with open("rfid.txt", "a") as f:
                        f.write(buff)
                        f.write("\n")
                    
                    buff = ""
                    buff += str_log + " "
                    
                    del buff_list[:]
                    buff_list.append(str_log)
                else:
                    buff += str_log + " "
                    buff_list.append(str_log)  
                 
            except Exception:
                read = False  
                 
        sent_read_cmd(ser)
        
def validate_rfid(rfid):
    '''Check rfid listed on server
    '''
    valid = False
    with open("tester.txt", "r") as f:
        for tester in f:
            if tester == rfid_str:
                valid = True
                break
            
    return valid
    
if __name__ == "__main__":
    read_rfid()
