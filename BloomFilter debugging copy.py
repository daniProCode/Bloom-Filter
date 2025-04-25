import hashlib
import csv
import sys
import array
import math

def addToBitArray(email, k):           # k = number of hashes
    hash_object1 = hashlib.sha256(email.encode()) 
    digest1 = int.from_bytes(hash_object1.digest(), 'big')
    hash_object2 = hashlib.sha1(email.encode())
    digest2 = int.from_bytes(hash_object2.digest(), 'big')
    hash_8bit = 0
    
    for i in range(k):
        hash_8bit = (digest1 + i * (digest2)) % total_bits
        setBit(bitMap, hash_8bit)
        hash_8bit = 0

def checkBitArray(email, k):
    hash_object1 = hashlib.sha256(email.encode()) 
    digest1 = int.from_bytes(hash_object1.digest(), 'big')
    hash_object2 = hashlib.sha1(email.encode())
    digest2 = int.from_bytes(hash_object2.digest(), 'big')
    hash_8bit = 0

    # for i in range(k):
    for i in range(k):
        hash_8bit = (digest1 + i*(digest2)) % total_bits
        if testBit(bitMap, hash_8bit) == False:
            print(bitMap[hash_8bit%len(bitMap)])
            return False
    # hash_8bit = 0

    return True
    

def makeBitArray(bitSize, fill = 0):
    intSize = bitSize >> 5                  # number of 32 bit integers
    if (bitSize & 31):                      # if bitSize != (32 * n) add
        intSize += 1                        #    a record for stragglers
    if fill == 1:
        fill = 4294967295                                 # all bits set
    else:
        fill = 0                                      # all bits cleared

    bitArray = array.array('I')          # 'I' = unsigned 32-bit integer
    bitArray.extend((fill,) * intSize)
    return(bitArray)

  # testBit() returns a nonzero result, 2**offset, if the bit at 'bit_num' is set to 1.
def testBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    return(array_name[record] & mask)

# setBit() returns an integer with the bit at 'bit_num' set to 1.
def setBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] |= mask


db_file = "db.csv"
input_file = 'input.csv'
db_list = []

with open(db_file, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    total_bits = 0
    for row in reader:
        if i == 0:
            i+=1
            continue
        db_list += row

    total_bits = int(-1*math.ceil((math.log(0.000000001) * len(db_list)) / (math.log(2)**2)))     # Formula to determine the number of bits needed in the array
    total_hashes = int(math.ceil(total_bits/len(db_list) * math.log(2)))                    # Formula for the number of hashes that will be used

    bitMap = makeBitArray(total_bits, 0)

    for email in db_list:
        addToBitArray(email,total_hashes)

with open(input_file, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for row in reader:
        if i == 0:
            i+=1
            continue
        
        if checkBitArray(row[0], total_hashes):
            print(f"{row[0]},Probably in the DB")

        else:
            print(f"{row[0]},Not in the DB")
        
