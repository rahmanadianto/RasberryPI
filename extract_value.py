#!/usr/bin/python3

'''
    Data format
    @00FA08000020000000000FC00|0102|82|000000|0001|04D2|02*
                                A   B   C       D   E   
    A = Command code (bit 26-29)
    B = Memory area code (bit 30-31)
    C = Address (bit 32-37)
    D = Number of element (bit 38-41)
    E = Data (bit 42 -(len - 3)) {max 1068 character}
'''

def extract_str(data):
    '''Extract data from single data with FINS protocol

    Return: [address_code, begin_address, number, value]
    '''
    if (data.find("0102", 26, 30) != -1):
        address_code = data[30:32]
        begin_address = data[32:38]
        number = str(int(data[38:42], 16))
        value = data[42:len(data) - 3]
        return [address_code, begin_address, number, value]
    else:
        return []

def extract_file(file_in, file_out):
    '''Extract data from file data with FINS protocol

    Return: result.txt
    '''
    with open(file_in, "r") as file_in:
        fins_list = file_in.read().splitlines()
        with open(file_out, "w") as file_out:
            for fins in fins_list:
                rstrip = fins.replace("\n", "").replace("\r","")
                result = extract_str(rstrip)
                #check if result not empty
                if result:
                    file_out.write(",".join(result))
                    file_out.write("\n")

