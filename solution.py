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
    print('vstup')
    print(format(x, '032b'))
    x = (x & 1) << N + 1 | x << 1 | x >> N - 1
    print('shift')
    print(format(x, '032b'))

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


def compareCandiadtesInLists(cand, base, i):
    print('kandidat do pice')
    print(cand)
    print(((cand | 17179869184) & 0x3))
    print('base do pice')
    print(base)
    print((((base | 17179869184) & (0x6 << i - 1)) >> i))
    return ((cand | 17179869184) & 0x3) == (((base | 17179869184) & (0x6 << i - 1)) >> i)


def getNewElement(cand, base, i):
    print('base')
    print(format(base, '010b'))
    print('cand')
    print(format(cand, '010b'))
    value =  ((((cand | 17179869184) & 0x4) << i) | base)
    print('value')
    print(format(value, '010b'))
    return value


def compareLists(final_list, cand, i):
    new_final = [0 for x in range(4)]
    print('rrrrrrrcand')
    print(cand)
    # print('rrrrrrfinal_list')
    # print(final_list)
    j = 0
    print ('bit', final_list)
    for candidate in cand:
        for final in final_list:
            value = compareCandiadtesInLists(candidate, final, i)
            if value:
                print('rrrrrrrj')
                print(j)
                new_final[j] = getNewElement(candidate, final, i)
                j += 1
                break
        
        # print(new_final)
    # print('-------------------------------')
    return new_final
            

    
def reverseStep(y):
    x = int.to_bytes(y, 32, 'little')
    final_str = []
    j = 0
    i = 0;
    for byte in x:
        candidate_list = -1
        # print(format(byte, '08b'))
        for bit in iterate_bits(byte):
            # print(format(bit, '08b'))
            # print('jeden bit')
            # print(bit)
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
        # for candidate in final_list:
            # print(candidate)
        # print('--------------------------')
        # final_str += [final_list]
    return final_list
            


print('step')
original = step(int.from_bytes('KRY{qwertzuiopasdfghjklyxcvb}'.encode(),'little'));
print('vysledek')
print(format(original, '032b'))
print(original)
# print(original)
# print(original)
# original = int.to_bytes(original, 32, 'little');
# print(original)

print('vstup reversed')
print(format(57896048210183943711694069256019884739780995237677627382219717421555487039481, '032b'))


print('reversed')

final = reverseStep(57896048210183943711694069256019884739780995237677627382219717421555487039481)
print(final)



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
