from time import sleep

from serial_helper import connect_port

 
def init_rfid(ser):
    '''Sent initialization command bytes to rfid
    '''
    ser.write(b"\xfe")
    time.sleep(0.2)
    ser.write(b"\xfe")
    time.sleep(0.2)
    ser.write(b"\xe1")
    time.sleep(0.2)
    ser.write(b"\xc2")
    ser.write(b"\xff")
    time.sleep(0.2)
    ser.write(b"\x20")
    ser.write(b"\xc0")
    time.sleep(0.2)
    ser.write(b"\x40")
    ser.write(b"\x02")
    ser.write(b"\x02")
    ser.write(b"\xbc")
    ser.write(b"\x40")
    ser.write(b"\x02")
    ser.write(b"\x02")
    ser.write(b"\xbc")
    time.sleep(1)
    ser.write(b"\x40")
    ser.write(b"\x02")
    ser.write(b"\x06")
    ser.write(b"\xb8")
    time.sleep(1)
    ser.write(b"\x40")
    ser.write(b"\x03")
    ser.write(b"\x0a")
    ser.write(b"\x01")
    ser.write(b"\xb2")
    time.sleep(1)

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

read_rfid():
    '''Listening to rfid
    '''
    ser = connect_port("/dev/ttyS0")
    buff = []

    init_rfid(ser)
        
    while True: 
         
        read = True;
     
        while read:
             
            receive = ser.read()
            str_log = ""

            try:
                receive_decode = receive.decode()
                str_log = str(hex(ord(receive_decode)))
            except ValueError:
                read = False
                print("No data")
                 
            if str_log == "0xee":
                 
                if len(buff) > 5:
                    rfid = buff[3:len(buff)-3]
                    rfid_str = ""
                    for x in rfid:
                        xv= x.replace("0x", "")
                        if len(xv) < 2:
                            xv = "0" + xv
                        rfid_str += xv
                    print(rfid_str)
                 
                with open("rfid.txt", "a") as f:
                    f.write(" ".join(buff))
                    f.write("\n")
                 
                del buff[:]

            buff.append(str_log)   
                 
        sent_read_cmd(ser)
