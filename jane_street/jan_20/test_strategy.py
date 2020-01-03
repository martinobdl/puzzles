import numpy as np

s=0
a2=None

while s<100: 
	a1 = 3
	if a2 is not None:
		a1 = 12 - a2   
	s+=a1
	print(s)
	if(s>=100):
		print("Pl1 loose")
	else:
		a2 = np.random.randint(1,10)   
		s+=a2
		if(s>=100):
			print("Pl2 loose")
	print(s)