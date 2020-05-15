import numpy as np
from sympy import *

n = 31
k = 11
err = 6
gen = [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
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

def computeSyndrome(r):
	rcv = []
	while r > 0:
		rcv.append(r % 2)
		r = int(r / 2)
	while len(rcv) < n:
		rcv.append(0) 
	rcv = np.flip(rcv)
	# print(rcv)

	rem = np.matmul(rcv, np.transpose(H))
	# print(rem)
	syn = 0
	for i in range(0, len(rem)):
		syn = syn + (abs(rem[i] % 2) * (2 ** (len(rem) - i - 1)))
	# print(syn)
	return int(syn)

bins = [[] for _ in range(0, err + 2)]


f = open("err_pat.txt")
for line in f:
	x = line.split()
	bins[int(x[1])].append(int(x[0]))
f.close()

err_pat = []

f = open("err_pat.txt", "w")
for i in range(0, err + 2):
	for j in range(0, len(bins[i])):
		err_pat.append(bins[i][j])
		# print(computeSyndrome(bins[i][j]))
# print(len(err_pat))

for i in range(0, len(err_pat)):
	print(computeSyndrome(err_pat[i]))
	f.write(str(err_pat[i]) + '\n')
f.close()
