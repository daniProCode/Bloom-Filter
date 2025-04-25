import hashlib
import csv
import sys
import array
import math

# addToBinary is a function that takes in a string (in this case for emails) 
# and a number of hashes (k). It takes the string and applies a double hashing method
# k times to activate certain bits in the bitMap array using the setBit function.
def addToBitArray(email, k):           
    # Use to different hsahing methods to implement double hashing, in case there isn't enough data
    # in the digest to reach k hashes.
    hash_object1 = hashlib.sha256(email.encode()) 
    digest1 = int.from_bytes(hash_object1.digest(), 'big')
    hash_object2 = hashlib.sha1(email.encode())
    digest2 = int.from_bytes(hash_object2.digest(), 'big')
    hash_bit = 0
    
    for i in range(k):
        # Double hash implementation 
        hash_bit = (digest1 + i * (digest2)) % total_bits
        setBit(bitMap, hash_bit)
        hash_bit = 0

# checkBitArray applies the same hashing method as the addBitArray function
# to check if certain bits in the array are activated (it checks this by using the
# testBit function below on each hash)
def checkBitArray(email, k):
    hash_object1 = hashlib.sha256(email.encode()) 
    digest1 = int.from_bytes(hash_object1.digest(), 'big')

    hash_object2 = hashlib.sha1(email.encode())
    digest2 = int.from_bytes(hash_object2.digest(), 'big')

    hash_bit = 0

    for i in range(k):
        hash_bit = (digest1 + i*(digest2)) % total_bits
        if not testBit(bitMap, hash_bit):
            return False

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

# Implementation of code
if len(sys.argv) > 2:           # Check if there are more than 2 arguments in command line
        db_file = sys.argv[1]           # Database file name    
        input_file = sys.argv[2]        # Inputs file name
        db_list = []                    # List for storing all emails from database
        try: 
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
                total_hashes = int(math.ceil(total_bits/len(db_list) * math.log(2)))                          # Formula for the number of hashes that will be used (k)

                bitMap = makeBitArray(total_bits, 0)        # Array of bits

                for email in db_list:
                    addToBitArray(email,total_hashes)

            with open(input_file, newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.reader(csvfile)
                i = 0
                for row in reader:
                    if i == 0:
                        i+=1
                        continue
                    
                    if checkBitArray(row[0], total_hashes):     # Applies check bit array to the current email
                        print(f"{row[0]},Probably in the DB")

                    else:
                        print(f"{row[0]},Not in the DB")
                    
        except FileNotFoundError:
            sys.exit(1)
            
