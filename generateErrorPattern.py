from itertools import islice

def main():
	f = open("check.csv")
	for line in f:
		print("%d %d" %(int(line, 2), countSetBits(int(line, 2))))

def countSetBits(num):
	if(num == 0):
		return 0
	else:
		return (num & 1) + countSetBits(num >> 1)

if __name__ == '__main__':
	main()