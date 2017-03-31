#!/usr/bin/python3

from time import sleep
import subprocess
import RPi.GPIO as GPIO

from serial_helper import connect_port
from hmi_logging import logging

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
    sleep(1)
    
def save_tester_tmp(data):
    print("Save tester")
    with open("tester_tmp.txt", "w") as f:
        f.write(data)

def save_product_tmp(data):
    print("Save product")
    with open("product_tmp.txt", "w") as f:
        f.write(data)

def read_rfid():
    '''Listening to rfid
    '''
    ser = connect_port("/dev/ttyS0")
    buff = ""
    buff_list = []
    #ignore first data from rfid
    first = True
    tester_tmp = ""
    
    #read mode : tester / product
    read_mode = 0

    init_rfid(ser)
        
    while True: 
        read = True;
        print("Waiting rfid data...", read_mode)
     
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
                        
                        if not first and tester_tmp != rfid_str:
                            print(rfid_str)
                            if read_mode == 0 and validate_tester(rfid_str):
                                save_tester_tmp(rfid_str)
                                tester_tmp = rfid_str
                                read_mode = 1
                                blink_led(11, True)
                            elif read_mode == 1 and validate_product(rfid_str):
                                save_product_tmp(rfid_str)
                                p = subprocess.call([
                                    "lxterminal",
                                    "-e",
                                    "python3 /home/pi/RasberryPI/hmi_logging.py"
                                ])
                                blink_led(13, True)
                                exit(0)
                            else:
                                if (read_mode == 0):
                                    blink_led(11, False)
                                else:
                                    read_mode = 0
                                    blink_led(13, False)
                                
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
        
def validate_tester(rfid):
    '''Check rfid listed on server
    '''
    valid = False
    with open("tester.txt", "r") as f:
        for tester in f:
            if tester.replace("\n","") == rfid:
                valid = True
                break
                
    print("Tester", valid)
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
                
    print("Product", valid)
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
            print("Blink ok")
        except Exception:
            print("Exception")
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
            print("Blink ok")
        except Exception:
            print("Exception")
            return

    
if __name__ == "__main__":
    read_rfid()
