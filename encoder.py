import numpy as np

n = 31
k = 11
gen = np.asarray([1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])
gen = np.flip(gen)

def bchEncoder(info):
	global gen
	msg = []
	for i in range(0, len(info)):
		msg.append(int(info[i]))
	# print("Message:")
	# print(msg)
	x_nk = [1] + [0 for _ in range(0, n - k)]
	x = np.polymul(msg, x_nk)
	# print(x_nk)
	[q, rem] = np.polydiv(x, gen)
	for i in range(0, len(rem)):
		rem[i] = abs(rem[i] % 2)
	# print(rem)
	if(len(rem) < n - k):
		rem = np.flip(rem).tolist()
		while(len(rem) < n - k):
			rem.append(0)
		rem = np.flip(rem)		
	code_word = rem.astype(int).tolist() + msg
	return code_word
	# print(type(code_word))



def binToStr(num):
	numStr = ""
	while num > 0:
		numStr = numStr + (num % 2).__str__()
		num = int(num / 2)
	while len(numStr) < 8:
		numStr = numStr + '0'
	return "".join(reversed(numStr))


str = input("Enter Message:")
info_str = ""
reg_block = []
for i in range(0, len(str)):
	info_str = info_str + binToStr(ord(str[i]))
while len(info_str) >= k:
	reg_block.append(bchEncoder(info_str[0:k]))
	info_str = info_str[k:len(info_str)]
while len(info_str) < k:
	info_str = info_str + '0'
reg_block.append(bchEncoder(info_str))

zeros = [0 for _ in range(n)] 

while len(reg_block) < n:
	reg_block.append(zeros)
reg_block = np.transpose(reg_block).tolist()
print(reg_block)





