import sys
import binascii
import os.path
import argparse
from pynverse import inversefunc

SUB = [0, 1, 1, 0, 1, 0, 1, 0]
N_B = 1
N = 8 * N_B


def step(x):
    # na konci se vzdy pridaji nejake jednicky
    x = (x & 1) << N+1 | x << 1 | x >> N-1
    # x = x << 1 | x >> N-1
    # print(format(x, '09b'))
    # print(format(x, '09b'))
    y = 0
    for i in range(N):
        # print('---------------------')
        # print(i)
        # print(format(((x >> i) & 7), '09b'))
        # print(SUB[(x >> i) & 7])
        # print(SUB[(x >> i) & 7] << i)
        y |= SUB[(x >> i) & 7] << i
        # print(i)
        print(y)
    return y

# def inverseStep(y):
    

# print(bin(int('10010101',2)))
# y = step(int('11011010',2))
step(218)



# print (format(y, '09b'))
# print(bin(y))

