import numpy as np
from sympy import *
n = 31
k = 11
gen = np.asarray([1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])
rcv = [1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0]
# rcv = [0 for _ in range(0, n)]
print("Received Codeword with Errors:")
print(rcv)

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
# print(H)

def computeSyndrome(r):
	rem = np.matmul(rcv, np.transpose(H))
	# print(rem)
	syn = 0
	for i in range(0, len(rem)):
		syn = syn + (abs(rem[i] % 2) * (2 ** (len(rem) - i - 1)))
	print(syn)
	return int(syn)

syn = computeSyndrome(rcv)
# print("Syndrome:")
# print bin(syn)
f = open("syndrome.txt")
syn_pat = f.readlines()
f.close()
try:
	x = syn_pat.index(str(syn) + '\n')
	f = open("err_pat.txt")
	err_pat = f.readlines()
	f.close()
	y = int(err_pat[x].replace('\n', ''))
	# print(bin(err))
	err = []
	while(y > 0):
		err.append(y % 2)
		y = int(y / 2)
	while(len(err) < n):
		err.append(0)
	err = err[::-1]
	for i in range(0, len(err)):
		rcv[i] = rcv[i] ^ err[i]
	print("Corrected  Codeword:")
	print(rcv)

	# print("Decoded Message:")
	# [msg, rem] = np.polydiv(rcv, gen)
	# for i in range(0, len(msg)):
		# msg[i] = int(abs(msg[i] % 2))
	# print(msg)
except ValueError:
	print("Not Found")
	x = -1