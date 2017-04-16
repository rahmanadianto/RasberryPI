#!/usr/bin/python3

from time import sleep
import subprocess
import RPi.GPIO as GPIO
import time

from serial_helper import connect_port
from hmi_logging import logging

GPIO.setmode(GPIO.BOARD)        
GPIO.setwarnings(False)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)

TIMEOUT = 5


def init_rfid(ser):
    '''Sent initialization command bytes to rfid
    '''
    print("Connecting rfid...")
    ser.write(b"\xbb")
    ser.write(b"\x00")
    ser.write(b"\x03")
    ser.write(b"\x00")
    ser.write(b"\x01")
    sleep(0.2)
    ser.write(b"\x00")
    ser.write(b"\x04")
    sleep(0.2)
    ser.write(b"\x7e")
    ser.write(b"\xbb")
    ser.write(b"\x00")
    ser.write(b"\x03")
    ser.write(b"\x00")
    ser.write(b"\x01")
    ser.write(b"\x01")
    ser.write(b"\x05")
    ser.write(b"\x7e")
    ser.write(b"\xbb")
    ser.write(b"\x00")
    ser.write(b"\x08")
    ser.write(b"\x00")
    ser.write(b"\x00")
    ser.write(b"\x08")
    ser.write(b"\x7e")
    sleep(1)

def sent_read_cmd(ser):
    '''Sent read command to rfid, request data from rfid
    '''
    ser.write(b"\xbb")
    ser.write(b"\x00")
    ser.write(b"\x27")
    ser.write(b"\x00")
    ser.write(b"\x03")
    ser.write(b"\x22")
    ser.write(b"\xff")
    ser.write(b"\xff")
    ser.write(b"\x4a")
    ser.write(b"\x7e")


def save_tester_tmp(data):
    print("Save tester")
    with open("tester_tmp.txt", "w") as f:
        f.write(data)


def save_product_tmp(data):
    print("Save product")
    with open("product_tmp.txt", "w") as f:
        f.write(data)

def rfid_list2str(rfid):
    rfid_str = ""
    for x in rfid:
        xv= x.replace("0x", "")
        if len(xv) < 2:
            xv = "0" + xv
        rfid_str += xv
    return rfid_str

def read_rfid():
    '''Listening to rfid
    '''
    ser = connect_port("/dev/ttyS0", 115200)
    buff = []
    tester_true = ""
    tester_false = ""
    product_true = ""
    product_false = ""
    mode = 1
    
    # timout
    start = 0
    
    #ignore first data from rfid
    first = True

    init_rfid(ser)
    print("Mode", mode)
    while True: 
        read = True;
        while read:
            receive = ser.read()
            str_log = ""
            
            if (time.time() - start >= TIMEOUT and start != 0):
                mode = 1
                print("Timeout, switch to mode 1")
                start = 0
            
            try:
                str_log = str(hex(ord(receive)))
                if str_log == "0xbb":
                    if len(buff) > 8:
                        rfid_str = rfid_list2str(buff[8:len(buff)-4])
                        if not first:
                            if mode == 1 and validate_tester(rfid_str):
                                print(rfid_str)
                                mode = 2
                                tester_true = rfid_str
                                blink_led(11, True)
                                #print("case 1")
                                print("Mode", mode)
                                start = time.time()
                            elif mode == 2 and not validate_product(rfid_str) and rfid_str == tester_true:
                                #print("case 2")
                                pass
                            elif mode == 2 and not validate_product(rfid_str) and rfid_str != tester_true:
                                print(rfid_str)
                                mode = 1
                                blink_led(13, False)
                                product_false = rfid_str
                                #print("case 3")
                                print("Mode", mode)
                                start = 0
                            elif mode == 2 and validate_product(rfid_str):
                                print(rfid_str)
                                mode = 1
                                start = 0
                                product_true = rfid_str
                                blink_led(13, True)
                                subprocess.call([
                                    "lxterminal",
                                    "-e",
                                    "python3 /home/pi/RasberryPI/hmi_logging.py"
                                ])   
                                #print("case 4")
                                print("Mode", mode)
                            elif mode == 1 and not validate_tester(rfid_str) and rfid_str == product_false:
                                #print("case 5")
                                pass
                            elif mode == 1 and not validate_tester(rfid_str) and rfid_str != product_true and rfid_str != tester_false:
                                print(rfid_str)
                                blink_led(11, False)
                                tester_false = rfid_str
                                #print("case 6")
                        first = False
                            
                    with open("rfid.txt", "a") as f:
                        f.write(" ".join(buff))
                        f.write("\n")
                    
                    del buff[:]
                    buff.append(str_log)
                else:
                    buff.append(str_log)  
                 
            except Exception:
                read = False 
                
        sent_read_cmd(ser)
  
        
def validate_tester(rfid):
    '''Check rfid listed on server
    '''
    valid = False
    with open("tester.txt", "r") as f:
        for tester in f:
            if tester.replace("\n","") == rfid:
                valid = True
                break
    return valid


def validate_product(rfid):
    '''Check rfid listed on server
    '''
    valid = False
    with open("product.txt", "r") as f:
        for product in f:
            product = product.split(",")
            if product[0] == rfid:
                valid = True
                break
    return valid
   
    
def blink_led(port, valid):
    if valid:
        try:
            GPIO.output(port,True)    
            sleep(0.05)          
            GPIO.output(port,False)
            sleep(0.05)          
            GPIO.output(port,True)
            sleep(0.05)
            GPIO.output(port,False)    
            sleep(0.05)          
            GPIO.output(port,True)
            sleep(0.05)
            GPIO.output(port,False)
            print("Blink True")
        except Exception:
            print("Blink True Exception")
            return
    else:
        try:
            GPIO.output(port,True)    
            sleep(0.2)          
            GPIO.output(port,False)
            sleep(0.2)
            GPIO.output(port,True)    
            sleep(0.2)
            GPIO.output(port,False)
            print("Blink False")
        except Exception:
            print("Blink False Exception")
            return

    
if __name__ == "__main__":
    read_rfid()
