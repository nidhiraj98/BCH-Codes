f = open("syndrome.txt")
syn_pat = f.readlines()
f.close()

if(len(syn_pat) == len(set(syn_pat))):
	print("Correct")
else:
	print("Incorrect")