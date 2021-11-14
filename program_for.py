import argparse, sys
import numpy as np
import csv
import os

# parser = argparse.ArgumentParser()
# parser.add_argument("-d", "--datafile", dest="datafile", required=True,
#                     help="File location of the relevant datafile")
# parser.add_argument("-l", "--type", dest="data_type", required=True,
#                     help="Data type of datafile ('int8', 'int16', 'int32', 'int64')")
# parser.add_argument("-t", "--task", dest="task", required=True,
#                     help="Specify whether to encode or decode the given data ('en' : encode, 'de' : decode)")


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


def encode(path, data_type):
    offset = 4
    content = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row = row[0]
            content.append(row)
    content = np.array(content).astype(int)
    frame = int(np.median(content))
    print("Frame:", frame)
    output_file = "%sfor" % path[:-3]

    if os.path.exists(output_file):
        os.remove(output_file)

    i = 0
    with open(output_file, 'ab') as f:
        f.write(frame.to_bytes(1, byteorder='big', signed=True))
        for row in content:
            enc = row - frame
            if exception(enc, offset):
                nbytes, nbits = bits_to_byte(data_type)
                escape = int('-' + '1'*(nbits-1), 2)-1
                f.write(escape.to_bytes(nbytes, byteorder='big', signed=True))  # write escape code (all bits 1)
                f.write(int(row).to_bytes(nbytes, byteorder='big', signed=True))  # write original value (uncompressed)
                i += 1
            else:
                f.write(int(enc).to_bytes(1, byteorder='big', signed=True))  # write compressed value
        # print("exceptions occurred:", i)


def decode(path, data_type):
    input_file = "%sfor" % path[:-3]
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
            print(val)
            i += 1
            # if i > 30:
            #     break


def main():
    # args = parser.parse_args()

    # path = args.datafile
    # data_type args.task
    data_type = "int8"
    data_types = ["int32", "int64"]
    file_names = ["linenumber-", "quantity-", "tax-", "extendedprice-"]
    for data_type in data_types:
        for file_name in file_names:

            path = r"C:\Users\Stand\Downloads\ADM-2021-Assignment-3-data-T-SF-1\ADM-2020-Assignment-2-data-T-SF-1\l_" + f"{file_name}{data_type}.csv"

            task = "en"

            if task == "en":
                encode(path, data_type)
            elif task == "de":
                decode(path, data_type)

            task = "de"
            if task == "en":
                encode(path, data_type)
            elif task == "de":
                decode(path, data_type)


if __name__ == '__main__':
    main()