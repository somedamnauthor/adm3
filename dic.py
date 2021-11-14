
import sys
import numpy as np
import pandas as pd
from collections import Counter
import os
import csv 
import ast
import time



# read arguments passed
n = len(sys.argv)
print("Total arguments passed:", n)
 
# print arguments passed
print("\nName of Python script:", sys.argv[0])

arg =[]

for i in range(1, n):
    print(sys.argv[i], end = " ")
    arg.append(sys.argv[i])

en_de = arg[0]     
print("\n\encode/decode: ", en_de)
compression_tech = arg[1]
print("\n\compression technique: ", compression_tech)
data_type = arg[2]
print("\n\input data type: ", data_type)
path_to_file = arg[3]
print("\n\path to file: ", path_to_file)
tic = time.time()



#for dictionary compressions/decompression

def dic_en_string(): 
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
        with open(str(path_ )+ "/" + str(compression_tech) + "_" + file_name, "w", newline ='') as fr:
            print (str(key_list).replace('[', '').replace(']', '').replace(' ', ''), file = fr)
            print (str(val_list).replace('[', '').replace(']', '').replace(' ', '').replace("'", ""), file = fr)
            for x in encoded_data:	
                print(x , file = fr)

        toc = time.time()
        print ("Dictionary Encoding is complete, please check original folder for output file")
        print("total time for encoding of " + str(file_name) +" is " + str(toc-tic))

def dic_en_int():
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
        with open(str(path_ )+ "/" + str(compression_tech) + "_" + file_name, "w", newline ='') as fr:
            print (str(key_list).replace('[', '').replace(']', '').replace(' ', ''), file = fr)
            print (str(val_list).replace('[', '').replace(']', '').replace(' ', '').replace("'", ""), file = fr)
            for x in encoded_data:	
                print(x , file = fr)
        
        toc = time.time()
        print ("Dictionary Encoding is complete, please check original folder for output file")
        print("total time for encoding of " + str(file_name) +" is " + str(toc-tic))
                                       
def dic_de():
    print("decoding")
    #read data from csv file and add index column
    col= ["val"]
    file_ = pd.read_csv(str(path_to_file), engine='python', header = None)


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
    toc = time.time()
    print("total time for decoding of " + str(file_name) +" is " + str(toc-tic))

                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
if compression_tech == 'dic':
    if en_de == "en":
        
        #read data from csv file and add index column
        col= ["val"]
        file_ = pd.read_csv(str(path_to_file), names=col , engine='python')
        file_.index = [x for x in range(1, len(file_.values)+1)]
        #print(file_)

        #split path to file and file name from path_file arguments passed
        path_, file_name = os.path.split(os.path.abspath(path_to_file))

        #for string
        if data_type == "string":
            dic_en_string()
                 
        #for int types
        elif data_type == "int8" or "int16" or "int32" or "int64": 
            dic_en_int()

        else:
            print ("please input valid data type")
            
            

        
    elif en_de == "de":
        #for all data types
        dic_de()
