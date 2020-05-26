import numpy as np
from sympy import Matrix
import math
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


def BCH_Decoder(rcv):
    global syn_pat
    global err_pat
    syn = computeSyndrome(rcv)
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
        rcv[j] = rcv[j] ^ err[j]
    return rcv

def main():
    rB = 500 * (10**6)
    tB = 1 / rB
    kB = 1.38 * (10 ** (-23))
    rL = 100
    tE = 256
    b = 2 * rB
    sigma = math.sqrt(4 * kB * tE * b/ rL)
    const = [0, 1]
    sigmaX = math.sqrt(0.165)
    muX = -(sigmaX **  2)
    eta = 0.15
    errRate = []
    pT = range(-15, -12)
    samples = 2

    for power in pT:
        print("Encoding Type: ", n, k)
        error = 0
        for sample in range(1, samples):
            info = [random.randrange(2) for _ in range(k)]
            print("Message Vector:                  ", info)
            info_str = [str(i) for i in info]
            info_str = "".join(info_str)
            codeword = BCH_Encoder(info_str)
            print("Codeword generated:              ",codeword)
            codewordChannel = []
            for code in codeword:
                r = random.gauss(muX, sigmaX)
                hsr = math.exp(2 * r)
                esr = random.gauss(0, 1)
                ysr = eta * hsr * math.sqrt(10 **(power * 0.1) * tB) * code + sigma * esr
                dec = 10 ** 90
                for i in range(2):
                    dis  = (ysr - eta * hsr * math.sqrt(10 ** (power * 0.1) * tB) * const[i]) ** 2
                    if dis < dec:
                        dec = dis
                        x1 = const[i]
                codewordChannel.append(x1)
            print("Received vector after channel:   ",codewordChannel)
            decoded = BCH_Decoder(codewordChannel)
            print("Codeword after error correction: ",decoded)
            msgEst = decoded[n - k: ]
            print("Decoded Message:                 ",msgEst)
            errPat = np.bitwise_xor(info, msgEst)
            error += sum(errPat)
            print()
        errRate.append(error / (k * sample))
    return errRate

if __name__ == "__main__":
    main()