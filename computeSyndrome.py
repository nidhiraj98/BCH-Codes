import numpy as np
import sys

n = 31
k = 11
err = 6
# rcv = np.asarray(r)
# rcv = np.flip(rcv)
gen = [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
x = np.zeros((n + 1, ), dtype = int)
x[0] = 1
x[n] = 1
[h, rem] = np.polydiv(x, gen)


def computeSyndrome(r):
	global gen
	syn = 0
	i = 0
	rcv = np.zeros((n, ))
	# print(rcv)
	while r > 0:
		rcv[n - i - 1] = r % 2
		r = int(r / 2)
		i = i + 1
	[q, rem] = np.polydiv(rcv, gen)
	# print(rem)
	for i in range(0, len(rem)):
		syn = syn + (abs(rem[i] % 2) * (2 ** (len(rem) - 1)))
	return int(syn)


if __name__ == '__main__':
	print(computeSyndrome(int(sys.argv[1])))
	# while True:
		# computeSyndrome(int(input()))