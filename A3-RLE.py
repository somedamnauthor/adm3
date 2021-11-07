#!/usr/bin/env python
# coding: utf-8

#imports
import csv
import time
import sys

action = str(sys.argv[1])
technique = str(sys.argv[2])
dtype = str(sys.argv[3])
ipFilepath = str(sys.argv[4])
#ipFilepath = '../ADM-2020-Assignment-2-data-T-SF-1/l_suppkey-int16.csv'

print("Action:",action)
print("Technique:",technique)
print("Datatype:",dtype)
print("Input Filepath:",ipFilepath)


# ### String

# #### String Decode

def decode(our_message):
    decoded_message = ""
    i = 0
    j = 0
    # splitting the encoded message into respective counts
    while (i <= len(our_message) - 1):
        run_count = int(our_message[i])
        run_word = our_message[i + 1]
        # displaying the character multiple times specified by the count
        for j in range(run_count):
            # concatenated with the decoded message
            decoded_message = decoded_message+run_word
            j = j + 1
        i = i + 2
    return decoded_message




def string_decode(ipFilepath, opFilepath):
    
    with open(ipFilepath) as file:
        encodedLines = file.readlines()
        
    start = time.time()
    decoded_lines = []
    for line in encodedLines:
        decoded_lines.append(decode(line))
    end = time.time()
    print("Time for Decode:",str(end-start))
    
    decoded_file = open(opFilepath, "w")
    for line in decoded_lines:
        decoded_file.write(line)
    decoded_file.close()


# #### String encode


def encode_message(message):
    encoded_string = ""
    i = 0
    while (i <= len(message)-1):
        count = 1
        ch = message[i]
        j = i
        while (j < len(message)-1): 
#         '''if the character at the current index is the same as the character at the next index. If the characters are the same, the count is incremented to 1'''    
            if (message[j] == message[j + 1]): 
                count = count + 1
                j = j + 1
            else: 
                break
        '''the count and the character is concatenated to the encoded string'''
        encoded_string = encoded_string + str(count) + ch
        i = j + 1
    return encoded_string



def string_encode(ipFilepath, opFilepath):

    with open(ipFilepath) as file:
        lines = file.readlines()
        
    start = time.time()
    encoded_lines = []
    for line in lines:
        encoded_lines.append(encode_message(line))
    end = time.time()
    print("Time for Encode:",str(end-start))
    
    encoded_file = open(opFilepath, "w")
    for line in encoded_lines:
        encoded_file.write(line)
    encoded_file.close()


# ##### Use encode-decode


# ipFilepath = '../ADM-2020-Assignment-2-data-T-SF-1/l_comment-string.csv'
# opFilepath = '../outputs/l_comment-string-en.csv'
# string_encode(ipFilepath, opFilepath)



# ipFilepath = '../outputs/l_comment-string-en.csv'
# opFilepath = '../outputs/l_comment-string-de.csv'
# string_decode(ipFilepath, opFilepath)


# ##### Use encode-decode again


# ipFilepath = '../ADM-2020-Assignment-2-data-T-SF-1/l_commitdate-string.csv'
# opFilepath = '../outputs/l_commitdate-string-en.csv'
# string_encode(ipFilepath, opFilepath)


# ipFilepath = '../outputs/l_commitdate-string-en.csv'
# opFilepath = '../outputs/l_commitdate-string-de.csv'
# string_decode(ipFilepath, opFilepath)


# ### int8

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


# ##### Use encode/Decode

# ipFilepath = '../ADM-2020-Assignment-2-data-T-SF-1/l_discount-int8.csv'
# opFilepath = '../outputs/l_discount-int8-en.csv'
# int8_encode(ipFilepath, opFilepath)


# ipFilepath = '../outputs/l_discount-int8-en.csv'
# opFilepath = '../outputs/l_discount-int8-de.csv'
# decode_int8(ipFilepath, opFilepath)


# ##### Use encode/Decode Again

# ipFilepath = '../ADM-2020-Assignment-2-data-T-SF-1/l_linenumber-int8.csv'
# opFilepath = '../outputs/l_linenumber-int8-en.csv'
# int8_encode(ipFilepath, opFilepath)


# ipFilepath = '../outputs/l_linenumber-int8-en.csv'
# opFilepath = '../outputs/l_linenumber-int8-de.csv'
# decode_int8(ipFilepath, opFilepath)


# ##### Use encode/Decode Again

# ipFilepath = '../ADM-2020-Assignment-2-data-T-SF-1/l_quantity-int8.csv'
# opFilepath = '../outputs/l_quantity-int8-en.csv'
# int8_encode(ipFilepath, opFilepath)


# ipFilepath = '../outputs/l_quantity-int8-en.csv'
# opFilepath = '../outputs/l_quantity-int8-de.csv'
# decode_int8(ipFilepath, opFilepath)


# ### int16

# ##### Encode

#https://stackoverflow.com/questions/46572023/run-length-encoding-python
from itertools import chain, groupby

def run_length(iterable):
    return list(chain.from_iterable(
        (val[:-1], len([*thing]))
        for val, thing in groupby(iterable)
    ))



def int16_encode(ipFilepath, opFilepath):
    
    with open(ipFilepath) as file:
        lines = file.readlines()
        
    start = time.time()
    encodedList = run_length(lines)
    encodedStr = ''
    for i in encodedList:
        encodedStr+=str(i)+' '
    end = time.time()
    print("Time for Encode:",str(end-start))
        
    encoded_file = open(opFilepath, "w")
    n = encoded_file.write(encodedStr)
    encoded_file.close()


# ##### Decode


def int16_decode(ipFilepath, opFilepath):
    
    with open(ipFilepath) as file:
        lines = file.readlines()
        
    start = time.time()
    tlist = lines[0].split()
    decStr = ''
    for i in range(0, len(tlist)):
        if i%2!=0:
            mul = int(tlist[i])
            for j in range(0, mul):
                decStr+=tlist[i-1]+'\n'
    end = time.time()
    print("Time for Decode:",str(end-start))
    
    decoded_file = open(opFilepath, "w")
    for line in decStr:
        decoded_file.write(line)
    decoded_file.close()


# ##### Trying Encode/Decode

# ipFilepath = '../ADM-2020-Assignment-2-data-T-SF-1/l_suppkey-int16.csv'
# opFilepath = '../outputs/l_suppkey-int16-en.csv'
# int16_encode(ipFilepath, opFilepath)


# ipFilepath = '../outputs/l_suppkey-int16-en.csv'
# opFilepath = '../outputs/l_suppkey-int16-de.csv'
# int16_decode(ipFilepath, opFilepath)


# ipFilepath = '../ADM-2020-Assignment-2-data-T-SF-1/l_linenumber-int8.csv'
# opFilepath = '../outputs/l_linenumber-int16-en.csv'
# int16_encode(ipFilepath, opFilepath)


# ipFilepath = '../outputs/l_linenumber-int16-en.csv'
# opFilepath = '../outputs/l_linenumber-int16-de.csv'
# int16_decode(ipFilepath, opFilepath)


# # Combined in 1 function:

# #arguments
# action = 'en'
# technique = 'rle'
# dtype = 'int16'
# ipFilepath = '../ADM-2020-Assignment-2-data-T-SF-1/l_suppkey-int16.csv'
# # ipFilepath = '../outputs/out.csv'


def execEncDec(action, technique, dtype, ipFilepath):
    
    opFilepath = '../outputs/out.csv'
    
    if technique != 'rle':
        return 0
    
    if dtype=='int8':
        
        if action == 'en':
            int8_encode(ipFilepath, opFilepath)
            
        elif action == 'de':
            int8_decode(ipFilepath, opFilepath)
    
    elif dtype == 'int16' or dtype == 'int32' or dtype == 'int64':
        
        if action == 'en':
            int16_encode(ipFilepath, opFilepath)
            
        elif action == 'de':
            int16_decode(ipFilepath, opFilepath)
            
    elif dtype == 'string':
        
        if action == 'en':
            string_encode(ipFilepath, opFilepath)
            
        elif action == 'de':
            string_decode(ipFilepath, opFilepath)


execEncDec(action, technique, dtype, ipFilepath)

