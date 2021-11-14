#!/usr/bin/env python
# coding: utf-8

#imports
import csv
import time
import sys
import pandas as pd
import numpy as np
import os

action = str(sys.argv[1])
technique = str(sys.argv[2])
dtype = str(sys.argv[3])
ipFilepath = str(sys.argv[4])

opFilepath = 'out.csv'

print("Action:",action)
print("Technique:",technique)
print("Datatype:",dtype)
print("Input Filepath:",ipFilepath)
print("Output Filepath:",opFilepath)
print("\n\n")

""" RLE """

# ##### Encode

from itertools import chain, groupby

def run_length(iterable):
    return list(chain.from_iterable(
        (val[:-1], len([*thing]))
        for val, thing in groupby(iterable)
    ))


def rle_encode(ipFilepath, opFilepath):
    
    with open(ipFilepath) as file:
        lines = file.readlines()
        
    start = time.time()
    encodedList = run_length(lines)
    encodedStr = ''
    for i in encodedList:
        encodedStr+=str(i)+'#'
    end = time.time()
    print("Time for Encode:",str(end-start))
        
    encoded_file = open(opFilepath, "w")
    n = encoded_file.write(encodedStr)
    encoded_file.close()


# ##### Decode


def rle_decode(ipFilepath, opFilepath):
    
    with open(ipFilepath) as file:
        lines = file.readlines()
        
    start = time.time()
    tlist = lines[0].split(sep='#')
    decStr = ''
    for i in range(0, len(tlist)):
        if i%2!=0:
            mul = int(tlist[i])
            for j in range(0, mul):
                decStr+=tlist[i-1]+'\n'
    end = time.time()
    print("Time for Decode:",str(end-start))

    print("Decoded:\n")
    print(decStr)
    
    decoded_file = open(opFilepath, "w")
    for line in decStr:
        decoded_file.write(line)
    decoded_file.close()



#RLE Modified - Works only for single digit numbers, but works better than standard RLE
# #### Encode

def encode_ints(data):
    encoding = ''
    prev_char = ''
    count = 1

    if not data: return ''

    for char in data:
        # If the prev and current characters
        # don't match...
        if char != prev_char:
            # ...then add the count and character
            # to our encoding
            if prev_char:
                encoding += str(count) + prev_char
            count = 1
            prev_char = char
        else:
            # Or increment our counter
            # if the characters do match
            count += 1
    else:
        # Finish off the encoding
        encoding += str(count) + prev_char
        return encoding


def int8_encode(ipFilepath, opFilepath):
    
    with open(ipFilepath) as file:
        lines = file.readlines()
    
    start = time.time()
    enc = ''
    for line in lines:
        num = int(line[:-1])
        if num <= 9:
            enc+=str(line[:-1])
        elif num == 10:
            enc+='z'
        elif num == 13:
            enc+='v'
        elif num == 48:
            enc+='w'
        elif num == 49:
            enc+='x'
        elif num == 50:
            enc+='y'
        else:
            enc+=chr(num)
            
    enc_op = encode_ints(enc)
    end = time.time()
    print("Time for encode:",str(end-start))
    
    encoded_file = open(opFilepath, "w")
    n = encoded_file.write(enc_op)
    encoded_file.close()


# #### Decode

def int_decode(data):
    i = 1
    dec = ''
    while(i<len(data)):
        for j in range(0, int(data[i-1])):
            dec+=data[i]
        i+=2
    return dec


def int8_decode(ipFilepath, opFilepath):
    
    with open(ipFilepath) as file:
        lines = file.readlines()

    enc_lines = lines[0]
    
    start = time.time()
    
    decoded_string = int_decode(enc_lines)
    
    decoded_list = []
    for ch in decoded_string:
        x = ord(ch)
        if x == 122:
            decoded_list.append(10)
        elif x == 118:
            decoded_list.append(13)
        elif x == 119:
            decoded_list.append(48)
        elif x == 120:
            decoded_list.append(49)
        elif x == 121:
            decoded_list.append(50)
        elif x >=48 and x <= 57:
            decoded_list.append(x-48)
        else:
            decoded_list.append(x)
            
    end = time.time()
    print("Time for Decode:",str(end-start))
            
    decoded_file = open(opFilepath, "w")
    for line in decoded_list:
        decoded_file.write(str(line)+"\n")
    decoded_file.close()

""" BIN """

def en_int8_bin(ipFilepath, opFilepath):
    df = pd.read_csv(ipFilepath)
    start_time = time.time()
    df = df.applymap(lambda x: x.to_bytes(1, 'little'))
    execution_time = time.time() - start_time
    df.to_csv(opFilepath)
    size = os.path.getsize(opFilepath)
    print(f'Size after encoding: {size}')
    print(f'Encoding time bin int8: {execution_time}')
    return df

def en_int16_bin(ipFilepath, opFilepath):
    df = pd.read_csv(ipFilepath)
    start_time = time.time()
    df =  df.applymap(lambda x: x.to_bytes(2, 'little'))
    execution_time = time.time() - start_time
    df.to_csv(opFilepath)
    size = os.path.getsize(opFilepath)
    print(f'Size after encoding: {size}')
    print(f'Encoding time bin int16: {execution_time}')
    return df

def en_int32_bin(ipFilepath, opFilepath):
    df = pd.read_csv(ipFilepath)
    start_time = time.time()
    df = df.applymap(lambda x: x.to_bytes(4, 'little'))
    execution_time = time.time() - start_time
    df.to_csv(opFilepath)
    size = os.path.getsize(opFilepath)
    print(f'Size after encoding: {size}')
    print(f'Encoding time bin int32: {execution_time}')
    return df

def en_int64_bin(ipFilepath, opFilepath):
    df = pd.read_csv(ipFilepath)
    start_time = time.time()
    df = df.applymap(lambda x: x.to_bytes(8, 'little'))
    execution_time = time.time() - start_time
    df.to_csv(opFilepath)
    size = os.path.getsize(opFilepath)
    print(f'Size after encoding: {size}')
    print(f'Encoding time bin int64: {execution_time}')
    return df


def de_int_bin(ipFilepath, opFilepath):
    df = pd.read_csv(ipFilepath)
    start_time = time.time()
    df = df.applymap(lambda x: int.from_bytes(x, 'little'))
    execution_time = time.time() - start_time
    print(f'decoding time bin int: {execution_time}')
    df.to_csv(opFilepath)
    return df


""" dif """

def exception(enc, offset):
    bin_enc = str(bin(enc))
    bin_enc = get_signed(bin_enc)
    return len(bin_enc) > offset


def bits_to_byte(data_type):
    if data_type == "int8":
        return 1, 8
    elif data_type == "int16":
        return 2, 16
    elif data_type == "int32":
        return 4, 32
    elif data_type == "int64":
        return 8, 64


def get_signed(enc):
    if enc[0:1] == '-':
        return "1" + enc[3:]
    else:
        return "0" + enc[2:]


def dif_encode(path, data_type):
    nbytes, nbits = bits_to_byte(data_type)
    offset = 4
    content = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row = row[0]
            content.append(row)
    content = np.array(content).astype(int)
    # output_file = "%sdif" % path[:-3]
    output_file = opFilepath

    if os.path.exists(output_file):
        os.remove(output_file)

    i = 0
    first = True
    with open(output_file, 'ab') as f:
        for row in content:
            if first:
                frame = int(row)
                f.write(frame.to_bytes(nbytes, byteorder='big', signed=True))
                first = False
                continue
            enc = row - frame
            frame = row
            if exception(enc, offset):
                escape = int('-' + '1'*(nbits-1), 2)-1
                f.write(escape.to_bytes(nbytes, byteorder='big', signed=True))  # write escape code (all bits 1)
                f.write(int(row).to_bytes(nbytes, byteorder='big', signed=True))  # write original value (uncompressed)
                i += 1
            else:
                f.write(int(enc).to_bytes(nbytes, byteorder='big', signed=True))  # write compressed value
        # print("exceptions occurred:", i)


def dif_decode(path, data_type):
    # input_file = "%sdif" % path[:-3]
    decList = []
    input_file = path
    nbytes, nbits = bits_to_byte(data_type)
    escape = int('-' + '1' * (nbits - 1), 2) - 1
    i = 0
    with open(input_file, "rb") as f:
        byte = f.read(1)
        frame = int.from_bytes(byte, "big", signed=True)
        print(frame)
        while byte != b"":
            byte = f.read(1)
            offset = int.from_bytes(byte, "big", signed=True)
            if offset == escape:
                byte = f.read(1)
                val = int.from_bytes(byte, "big", signed=True)
            else:
                val = offset + frame
            frame = val
            decList.append(val)
            print(val)
            i += 1
    
    decoded_file = open(opFilepath, "w")
    for line in decList:
        decoded_file.write(str(line)+"\n")
    decoded_file.close()


""" for """
def for_encode(path, data_type):
    nbytes, nbits = bits_to_byte(data_type)
    offset = 4
    content = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row = row[0]
            content.append(row)
    content = np.array(content).astype(int)
    frame = int(np.median(content))
    # print("Frame:", frame)
    # output_file = "%sfor" % path[:-3]
    output_file = opFilepath

    if os.path.exists(output_file):
        os.remove(output_file)

    i = 0
    with open(output_file, 'ab') as f:
        f.write(frame.to_bytes(nbytes, byteorder='big', signed=True))
        for row in content:
            enc = row - frame
            if exception(enc, offset):
                escape = int('-' + '1'*(nbits-1), 2)-1
                f.write(escape.to_bytes(nbytes, byteorder='big', signed=True))  # write escape code (all bits 1)
                f.write(int(row).to_bytes(nbytes, byteorder='big', signed=True))  # write original value (uncompressed)
                i += 1
            else:
                f.write(int(enc).to_bytes(nbytes, byteorder='big', signed=True))  # write compressed value
        # print("exceptions occurred:", i)


def for_decode(path, data_type):
    decList = []
    # input_file = "%sfor" % path[:-3]
    input_file = path
    nbytes, nbits = bits_to_byte(data_type)
    escape = int('-' + '1' * (nbits - 1), 2) - 1
    i = 0
    with open(input_file, "rb") as f:
        byte = f.read(1)
        frame = int.from_bytes(byte, "big", signed=True)
        print(frame)
        while byte != b"":
            byte = f.read(1)
            offset = int.from_bytes(byte, "big", signed=True)
            if offset == escape:
                byte = f.read(1)
                val = int.from_bytes(byte, "big", signed=True)
            else:
                val = offset + frame
            decList.append(val)
            print(val)
            i += 1

    decoded_file = open(opFilepath, "w")
    for line in decList:
        decoded_file.write(str(line)+"\n")
    decoded_file.close()


""" dic """

def dic_en_string(file_): 

    tic = time.time()

    #get the unique value
    pattern = pd.unique(file_['val'])
    #print(pattern)
    encoded_data = []
    i= 0
    dict1 = {}


    for item in pattern:
                dict1[i] = []   ##THIS IS THE DICTIONARY
                dict1[i].append(item) 
                i = i+1

    key_list = list(dict1.keys())
    val_list = list(dict1.values())
    for value in file_['val']:
            position = val_list.index([str(value)])
            encoded_data.append(key_list[position])   #THIS IS THE ENCODED DATA


    #write encoded data into file. 
    # with open(str(path_ )+ "/" + str(compression_tech) + "_" + file_name, "w", newline ='') as fr:
    with open(opFilepath, "w", newline='') as fr:
        print (str(key_list).replace('[', '').replace(']', '').replace(' ', ''), file = fr)
        print (str(val_list).replace('[', '').replace(']', '').replace(' ', '').replace("'", ""), file = fr)
        for x in encoded_data:	
            print(x , file = fr)

    toc = time.time()
    # print ("Dictionary Encoding is complete, please check original folder for output file")
    print("total time for encoding is " + str(toc-tic))


def dic_en_int(file_):

    tic = time.time()

    #get the unique value
    pattern = pd.unique(file_['val'])
    #print(pattern)
    encoded_data = []
    i= 0
    dict1 = {}


    for item in pattern:
                dict1[i] = []   ##THIS IS THE DICTIONARY
                dict1[i].append(item) 
                i = i+1

    key_list = list(dict1.keys())
    val_list = list(dict1.values())
    for value in file_['val']:
            position = val_list.index([value])
            encoded_data.append(key_list[position])   

    #write encoded data into file. 
    # with open(str(path_ )+ "/" + str(compression_tech) + "_" + file_name, "w", newline ='') as fr:
    with open(opFilepath, "w", newline='') as fr:
        print (str(key_list).replace('[', '').replace(']', '').replace(' ', ''), file = fr)
        print (str(val_list).replace('[', '').replace(']', '').replace(' ', '').replace("'", ""), file = fr)
        for x in encoded_data:	
            print(x , file = fr)
    
    toc = time.time()
    # print ("Dictionary Encoding is complete, please check original folder for output file")
    print("total time for encoding is " + str(toc-tic))
                                       

def dic_de(ipFilepath):

    tic = time.time()

    # print("decoding")
    #read data from csv file and add index column
    col= ["val"]
    file_ = pd.read_csv(str(ipFilepath), engine='python', header = None)


    #get the encoded data 
    data = file_.iloc[2:, 0]
    #print(data)

    #get keys and values from dictionary (from the first 2 rows of the file)
    keys = []
    for row in file_.iloc[0, 0:]:
        keys.append(int(row))

    values = []
    for row in file_.iloc[1, 0:]:
        values.append(row)        

    #recreate original dictionary
    dictionary = dict(zip(keys,values))


    key_list = list(dictionary.keys())
    val_list = list(dictionary.values())

    decoded_data = []
            #find coresponding dictionary item for each encoded value and append to final data
    for val in data:
        for key, value in dictionary.items(): 
            if int(val) == key: 
                 decoded_data.append(value)           
    #print final data           
    for x in decoded_data:
        print(x)

    decoded_file = open(opFilepath, "w")
    for line in decoded_data:
        decoded_file.write(str(int(line))+"\n")
    decoded_file.close()

    toc = time.time()
    print("total time for decoding is " + str(toc-tic))


"""************************************"""

""" MASTER FUNCTION """
def execEncDec(action, technique, dtype, ipFilepath):
    
    # opFilepath = 'out.csv'
    
    if technique == 'rle_mod':
        
        if action == 'en':
            int8_encode(ipFilepath, opFilepath)

        elif action == 'de':
            int8_decode(ipFilepath, opFilepath)

    elif technique == 'rle':

        if action == 'en':
            rle_encode(ipFilepath, opFilepath)

        elif action == 'de':
            rle_decode(ipFilepath, opFilepath)

    elif technique == 'bin':

        if action == 'en':

            if dtype == 'int8':
                en_int8_bin(ipFilepath, opFilepath)

            elif dtype == 'int16':
                en_int16_bin(ipFilepath, opFilepath)

            elif dtype == 'int32':
                en_int32_bin(ipFilepath, opFilepath)

            elif dtype == 'int64':
                en_int64_bin(ipFilepath, opFilepath)

            elif dtype == 'string':
                print("ERROR - Invalid technique for datatype")

        elif action == 'de':
            de_int_bin(ipFilepath, opFilepath)

    elif technique == 'dif':

        if action == 'en':
            dif_encode(ipFilepath, dtype)

        elif action == 'de':
            dif_decode(ipFilepath, dtype)

    elif technique == 'for':

        if action == 'en':
            for_encode(ipFilepath, dtype)

        elif action == 'de':
            for_decode(ipFilepath, dtype)

    elif technique == 'dic':

        path_to_file = ipFilepath
        data_type = dtype

        if action == 'en':

            #read data from csv file and add index column
            col= ["val"]
            file_ = pd.read_csv(str(path_to_file), names=col , sep='delimiter', engine='python')
            file_.index = [x for x in range(1, len(file_.values)+1)]
            #print(file_)

            #split path to file and file name from path_file arguments passed
            path_, file_name = os.path.split(os.path.abspath(path_to_file))

            #for string
            if data_type == "string":
                dic_en_string(file_)
                    
            #for int types
            elif data_type == "int8" or "int16" or "int32" or "int64": 
                dic_en_int(file_)

            else:
                print ("ERROR - Invalid technique for datatype")

        elif action == 'de':

            dic_de(ipFilepath)


""" CALL MASTER """
execEncDec(action, technique, dtype, ipFilepath)

