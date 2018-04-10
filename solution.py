#!/usr/bin/env python3

import argparse
import sys
import binascii
import array


# parser = argparse.ArgumentParser()
# parser.add_argument("key")
# args = parser.parse_args()

SUB = [0, 1, 1, 0, 1, 0, 1, 0]
N_B = 32
N = 8 * N_B
cand_0 = [0x0, 0x3, 0x5, 0x7]
cand_1 = [0x1, 0x2, 0x4, 0x6]

# Next keystream
def step(x):
#   x = (x & 1) << N + 1 | x << 1 | x >> N - 1
    y = 0
    for i in range(N):
        y |= SUB[(x >> i) & 7] << i
    return y


def iterate_bits(byte):
    for i in range(8):
        bit = byte & (0x1 << i)
        yield bit


def isBitOne(bit, i):
    return bit & (0x1 << i) == (0x1 << i)


# v kazdem cyklu bych mel mit jeden true, ale nedostavam ho...
def compareCandiadtesInLists(cand, base):
    print('can')
    print(bin((cand | 0x100) & 0x3))
    print('base')
    print(bin((base | 0x100) & 0x6))

    return ((cand | 0x100) & 0x3) == ((base | 0x100) & 0x6)


def getNewElement(cand, base, i):
    return ((((cand | 0x100) & 0x4) << i + 3) | base)


def compareLists(final_list, cand, i):
    new_final = []
    print('cand_arr')
    print(cand)
    for base in final_list:
        for candidate in cand:
            # print('candidate')
            # print(bin(candidate))
            # print('base')
            # print(bin(base))
            # print(compareCandiadtesInLists(candidate, base))
            value = compareCandiadtesInLists(candidate, base)
            print(value)
            if value:
                new_final.append(getNewElement(candidate, base, i))
        print('--------------------------------')

    return new_final
            

    
def reverseStep(y):
    x = int.to_bytes(y, 1, 'little')
    for byte in x:
        i = 0;
        candidate_list = -1

        for bit in iterate_bits(byte):
            if i == 0:
                if isBitOne(bit, i):
                    start_list = cand_1
                else:
                    start_list = cand_0
                final_list = start_list
            else:
                if isBitOne(bit, i):
                    candidate_list = cand_1
                else:
                    candidate_list = cand_0
                final_list = compareLists(final_list, candidate_list, i)

            i += 1
    return final_list
            


print('step')
print(step(int.from_bytes('a'.encode(),'little')));


print('reversed')
encoded = int.from_bytes('Y'.encode(), 'little')
print(reverseStep(encoded))


# # Keystream init
# keystr = int.from_bytes(args.key.encode(),'little')

# for i in range(N//2):
#   keystr = step(keystr)

#   # Encrypt/decrypt stdin2stdout 
#   plaintext = sys.stdin.buffer.read(N_B)
#   keystr = step(keystr)
#   print(binascii.hexlify((int.from_bytes(plaintext,'little') ^ keystr).to_bytes(N_B,'little')))

# sys.stdout.flush()
