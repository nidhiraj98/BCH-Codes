import numpy as np
from sympy import *
# import RPi.GPIO as GPIO
import time
import random

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(18,GPIO.OUT)
# GPIO.setup(4, GPIO.IN)

n = 31
k = 11
gen = np.asarray([1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])
x = np.zeros((n + 1, ), dtype = int)
x[0] = 1
x[n] = 1
[h, rem] = np.polydiv(x, gen)
for i in range(0, len(h)):
		h[i] = abs(h[i] % 2)
h = h.tolist()
while len(h) < n:
	h.append(0.0)
H = [[] for _ in range(0, n - k)]
for i in range(0, n - k):
	H[i] = [0.0 for _ in range(0, i)] + h[0: n - i]

H = Matrix(H)
[H, r] = H.rref()
H = abs(H % 2).tolist()
for i in range(0, n - k):
	H[i] = list(map(int, H[i]))

f = open("syndrome.txt")
syn_pat = f.readlines()
f.close()

f = open("err_pat.txt")
err_pat = f.readlines()
f.close()


def BCH_Encoder(info):
	global gen
	g = np.flip(gen)
	msg = []
	for i in range(0, len(info)):
		msg.append(int(info[i]))
	# print("Message:")
	# print(msg)
	x_nk = [1] + [0 for _ in range(0, n - k)]
	x = np.polymul(msg, x_nk)
	# print(x_nk)
	[q, rem] = np.polydiv(x, g)
	for i in range(0, len(rem)):
		rem[i] = abs(rem[i] % 2)
	# print(rem)
	if(len(rem) < n - k):
		rem = np.flip(rem).tolist()
		while(len(rem) < n - k):
			rem.append(0)
		rem = np.flip(rem)		
	code_word = rem.astype(int).tolist() + msg
	# print(code_word)
	return code_word

def binToStr(num):
	numStr = ""
	while num > 0:
		numStr = numStr + (num % 2).__str__()
		num = int(num / 2)
	while len(numStr) < 8:
		numStr = numStr + '0'
	return "".join(reversed(numStr))

# def RPi_Out(reg_blk):
# 	rcv_blk = [[] for _ in range(0, n)]
# 	# for i in range(0, n):
# 	# 	for j in range(0, n):
# 	# 		if reg_blk[i][j] == 1:
# 	# 			GPIO.output(18, GPIO.HIGH)
# 	# 		else:
# 	# 			GPIO.output(18, GPIO.LOW)
# 	# 		time.sleep(0.1)
# 	# 		if(GPIO.input(4)):
# 	# 			rcv_blk[i].append(1)
# 	# 		else:
# 	# 			rcv_blk[i].append(0)
# 	# 		GPIO.output(18, GPIO.LOW)
# 	rcv_blk = reg_blk
# 	rcv_blk = np.transpose(rcv_blk)
# 	BCH_Decoder(rcv_blk)

def computeSyndrome(r):
	global H
	rem = np.matmul(r, np.transpose(H))
	# print(rem)
	syn = 0
	for i in range(0, len(rem)):
		syn = syn + (abs(rem[i] % 2) * (2 ** (len(rem) - i - 1)))
	# print(syn)
	# print(type(syn))
	return int(syn)


def BCH_Decoder(rcv_blk):
	global syn_pat
	global err_pat
	corr_blk = [[] for _ in range(0, n)]
	rcv_blk = np.transpose(rcv_blk)
	for i in range(0, n):
		syn = computeSyndrome(rcv_blk[i])
		# print(str(syn))
		x = syn_pat.index(str(syn) + '\n')
		y = int(err_pat[x].replace('\n', ''))
		# print(bin(err))
		err = []
		while(y > 0):
			err.append(y % 2)
			y = int(y / 2)
		while(len(err) < n):
			err.append(0)
		err = err[::-1]
		for j in range(0, len(err)):
			rcv_blk[i][j] = rcv_blk[i][j] ^ err[j]
		corr_blk[i] = rcv_blk[i]

	corr_blk = np.asarray(corr_blk).tolist()
	# print("Decoded Block:")
	return corr_blk

f = open("testText.txt", "r")
string = f.readline()
print(string)
f.close()
info_str = ""
msg_count = 0
msgBlock = []
codewordBlock = []

print("Total Number of Characters: ", len(string))
for i in range(0, len(string)):
	x = bin(ord(string[i]))[2:]
	# print(x, string[i])
	while len(x) < 7:
		x = '0' + x
	info_str = info_str + x

# info = [random.randrange(2) for _ in range(k)]
# info = [str(i) for i in info]
# info_str = "".join(info)

while len(info_str) >= k:
	msgBlock.append(info_str[0:k])
	msg_count = msg_count + 1
	info_str = info_str[k:len(info_str)]

while len(info_str) < k:
	info_str = info_str + '0'

msgBlock.append(info_str)

# print(msgBlock)

for m in msgBlock:
	codewordBlock.append(BCH_Encoder(m))

while len(codewordBlock) %n != 0:
	codewordBlock.append([0 for _ in range(n)])

# print(codewordBlock)
print("Total Number of Encoded Blocks: ", int(len(codewordBlock)/n))
print("Encoding Type: ", n, k)
print()

rcvMsg = []
for i in range(0, len(codewordBlock), n):
	corrBlock = BCH_Decoder(np.transpose(codewordBlock[i: i + n]).tolist())
	for j in range(len(corrBlock)):
		rcvMsg = rcvMsg + corrBlock[j][n - k: ]

# print(rcvMsg)
msgStr = ""
zeros = [0 for _ in range(7)]
for j in range(0, len(rcvMsg), 7):
	x = rcvMsg[j: j + 7]
	# print(x)
	if x == zeros:
		break
	x = [str(m) for m in x]
	msgStr = msgStr + chr(int("".join(x), 2))

print(msgStr)

# print(rcvMsg)