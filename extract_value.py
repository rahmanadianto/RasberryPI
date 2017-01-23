#!/usr/bin/python3

'''
    Data format
    @00FA08000020000000000FC00|0102|82|000000|0001|04D2|02*
                                A   B   C       D   E   
    A = Command code (bit 26-29)
    B = Memory area code (bit 30-31)
    C = Address (bit 32-37)
    D = Number of element (bit 38-41)
    E = Data (bit 42-(len - 3)) {max 1068 character}
'''

with open("data.txt", "r") as file_in:
    fins_list = file_in.read().splitlines()
    for fins in fins_list:
        if (fins.find("0102", 26, 30) != -1):
            with open("result.txt", "a") as file_out:
                address_code = fins[30:32]
                begin_address = fins[32:38]
                hex_value = fins[42:len(fins) - 3]
                dec_value = int(hex_value, 16)
                file_out.write("Code memory: " + address_code + "\n")
                file_out.write("Beginning address: " + begin_address + "\n")
                file_out.write("Sending data: " + str(dec_value) + "\n\n")
