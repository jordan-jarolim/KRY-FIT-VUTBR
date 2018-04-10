#!/usr/bin/env python3

import sys
import binascii
import os.path
import argparse


dev = False

def readText(name):
    absolutePath = os.path.abspath(os.path.dirname(__file__))
    relativePath = os.path.join(absolutePath, name)
    file = open(relativePath, "rb") 
    text = file.read()
    file.close()
    return text


def bytes_xor(a, b) :
    return bytes(x ^ y for x, y in zip(a, b))

# read inputs
uncyphered = readText('in/bis.txt')
cyphered = readText('in/bis.txt.enc')

# xor inputs -> get pseudokey
xored = binascii.hexlify(bytes_xor(uncyphered, cyphered))

# print?
if dev == True:
    print(xored)

xored = xored.decode()


SUB = [0, 1, 1, 0, 1, 0, 1, 0]
N_B = 32
N = 8 * N_B


# def step(x):
#   x = (x & 1) << N+1 | x << 1 | x >> N-1
#   y = 0
#   for i in range(N):
#     y |= SUB[(x >> i) & 7] << i
    
#   return y


def step(y):
    x = 0
    for i in range(N):
        x |= SUB[(y >> N-i) & 7] << N-i
    
    x = (x & 1) << N+1 | x << 1 | x >> N-1

    return x


# def step(x):
#     # x = (x & 1) << N+1 | x << 1 | x >> N-1
#     # y = 0

#     for i in range(N):
#         if i == N:
#             y = 0 | (SUB[(x >> N-i) & 7] << N-i)
#         else:
#             y = y | (SUB[(x >> N-i) & 7] << N-i)



        
#     return y


# Keystream init
keystr = int.from_bytes(xored.encode(),'little')
for i in range(N//2):
  keystr = step(keystr)

# Encrypt/decrypt stdin2stdout 
#plaintext = sys.stdin.buffer.read(N_B)
keystr = step(keystr)
print(keystr)
#sys.stdout.buffer.write((int.from_bytes(plaintext,'little') ^ keystr).to_bytes(N_B,'little'))


  
