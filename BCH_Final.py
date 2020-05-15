import numpy as np
from sympy import *
# import RPi.GPIO as GPIO
import time

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

def RPi_Out(reg_blk):
	rcv_blk = [[] for _ in range(0, n)]
	# for i in range(0, n):
	# 	for j in range(0, n):
	# 		if reg_blk[i][j] == 1:
	# 			GPIO.output(18, GPIO.HIGH)
	# 		else:
	# 			GPIO.output(18, GPIO.LOW)
	# 		time.sleep(0.1)
	# 		if(GPIO.input(4)):
	# 			rcv_blk[i].append(1)
	# 		else:
	# 			rcv_blk[i].append(0)
	# 		GPIO.output(18, GPIO.LOW)
	rcv_blk = reg_blk
	rcv_blk = np.transpose(rcv_blk)
	BCH_Decoder(rcv_blk)

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
	print("Decoded Block:")
	print(corr_blk)

	msg = []
	msg_str = ""
	for i in range(0, n):
		msg = msg + corr_blk[i][n - k : ]
		# print(msg)
		val = 0
		for j in range(0, 8):
			val = val + msg[j] * (2 ** (7 - j))
		msg_str = msg_str + chr(val)
		if(val == 0):
			break
		msg = msg[8: ]
	print(msg_str)


string = input("Enter Message:")
info_str = ""
msg_count = 0
reg_blk = [[] for _ in range(0, n)]

for i in range(0, len(string)):
	info_str = info_str + binToStr(ord(string[i]))

while len(info_str) >= k:
	reg_blk[msg_count] = BCH_Encoder(info_str[0:k])
	msg_count = msg_count + 1
	info_str = info_str[k:len(info_str)]

while len(info_str) < k:
	info_str = info_str + '0'

reg_blk[msg_count] = BCH_Encoder(info_str)
msg_count = msg_count + 1

ext = [0 for _ in range(0, n)]
while msg_count < n:
	reg_blk[msg_count] = ext
	msg_count = msg_count + 1

reg_blk = np.transpose(reg_blk).tolist()
print("Encoding Done with interleaving")
print(reg_blk)
# BCH_Decoder(reg_blk)
RPi_Out(reg_blk)