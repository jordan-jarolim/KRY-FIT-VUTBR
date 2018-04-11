#!/usr/bin/env python3

import argparse
import sys
import binascii
import array
import os


# parser = argparse.ArgumentParser()
# parser.add_argument("key")
# args = parser.parse_args()

SUB = [0, 1, 1, 0, 1, 0, 1, 0]
N_B = 32
N = 8 * N_B

# Candidate lists
# If actualy parsed bit is 1/0, it is mapped to one of the following groups
# these groups are based on SUB array
cand_0 = [0x0, 0x3, 0x5, 0x7]
cand_1 = [0x1, 0x2, 0x4, 0x6]

# Next keystream
def step(x):
    # print('step')
    # print(x.bit_length())
    # print(format(x, 'b'))
    x = (x & 1) << N + 1 | x << 1 | x >> N - 1
    # print(x.bit_length())
    # print(format(x, 'b'))
    # print('----------------------------')
    y = 0
    for i in range(N):
        y |= SUB[(x >> i) & 7] << i
    return y

# Iterate bits in byte from right side
# Always returns 8-bit representation with bit marked on respective position
def iterate_bits(byte):
    for i in range(8):
        bit = byte & (0x1 << i)
        yield bit

# Check if given bit is 1
# Works with 8-bit bytes and compares given position only
def isBitOne(bit, i):
    return bit & (0x1 << i % 8) == (0x1 << i % 8)

# Compare last two bits of candidate with first two bits of base-list member
def compareCandiadtesInLists(cand, base, i):
    return ((cand) & 0x3) == (((base) & (0x6 << i - 1)) >> i)

# Append the most left bit of candidate to the left side of base-list member
def getNewElement(cand, base, i):
    value =  ((((cand) & 0x4) << i) | base)
    return value

# Try to match each candidate into base-list member
# If one candidate is mapped multiple times into one base-list member,
# all newly-generated members are kept. But unmapped members are thrown away
def compareLists(base_list, cand, i):
    new_final = [0 for x in range(4)]
    j = 0
    for candidate in cand:
        for final in base_list:
            value = compareCandiadtesInLists(candidate, final, i)
            if value:
                new_final[j] = getNewElement(candidate, final, i)
                j += 1
                break
    return new_final

# Choose best option to do shift
def choose_best(base_list):
    final = -1
    for option in base_list:
        if (option & (3 << 256) == (option & 3) << 256):
            final = option
            break;
    return final

# Shift selected option (reverse to 1st step operation)
def shift_chosen(chosen):
    print(chosen.bit_length())
    print(format(chosen, 'b'))
    # if (length > 257):
    #     length = 257
    # chosen = (int(bin(chosen)[-257:], 2)) >> 1
    chosen = chosen >> 1
    if (chosen.bit_length() >= 257):
        chosen = int(bin(chosen)[-256:], 2)
    return chosen

# Tranform int to string
def int_to_string(shifted):
    return int.to_bytes(shifted, 32, 'little').decode('utf-8')


# Reverse ste function    
def reverseStep(y):
    x = int.to_bytes(y, 32, 'little')
    final_str = []
    j = 0
    i = 0;
    for byte in x:
        candidate_list = -1
        for bit in iterate_bits(byte):
            if i == 0:
                if isBitOne(bit, i):
                    start_list = cand_1
                else:
                    start_list = cand_0
                    
                base_list = start_list
            else:
                if isBitOne(bit, i):
                    candidate_list = cand_1
                else:
                    candidate_list = cand_0
                base_list = compareLists(base_list, candidate_list, i)
            i += 1

    chosen = choose_best(base_list)
    shifted = shift_chosen(chosen)
    # stringified = int_to_string(shifted)
    return shifted
            


print('step')
original = int.from_bytes('KRY{qwertzuiopasdfghjklyxcvb}'.encode(),'little')

for i in range(N//2):
    original = step(original)

original = step(original)

print('vysledek')
print(format(original, 'b'))
print(original)

print('reversed')
final = 53732762364271725616554037660579309881140189147263019822410701712482392295930

for i in range(N//2):
    final = reverseStep(final)

final = reverseStep(final)

print(int_to_string(final))


# file = open(os.path.join('in/', "bis.txt"), "r")
# original = file.read()
# file.close()

# file = open(os.path.join('in/', "bis.txt.enc"), "r")
# enc = file.read()
# file.close()

# print(format(int.from_bytes(enc.encode(), 'little'), 'b'))

# original = int.from_bytes(original.encode(), 'little')
# print(format(original, 'b'))
# enc = int.from_bytes(enc.encode(), 'little')

# result = enc ^ original
# print (format(result, 'b'))

# for i in range(N//2):
#     result = reverseStep(result)

# result = reverseStep(result)
# print(int_to_string(result))






# final = [int.to_bytes(e, 32, 'little') for e in final]
# print (final)
# for byte in final:
    # print(int.from_bytes(byte.encode(), 'little'))
    # print(format(chr(byte), '08b'))
# print(''.join(final), '032b')

# # Keystream init
# keystr = int.from_bytes(args.key.encode(),'little')

# for i in range(N//2):
#   keystr = step(keystr)

#   # Encrypt/decrypt stdin2stdout 
#   plaintext = sys.stdin.buffer.read(N_B)
#   keystr = step(keystr)
#   print(binascii.hexlify((int.from_bytes(plaintext,'little') ^ keystr).to_bytes(N_B,'little')))

# sys.stdout.flush()
