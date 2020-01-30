with open('letter.txt','r') as f:
    lines = f.readlines()
lines.append("\n")

letter = []
parag = []
for line in lines:
    if line != "\n":
        parag.append(line)
    else:
        letter.append(parag)
        parag=[]

with open('key.txt','r') as f:
    for l in f.readlines():
        p,l,c = map(int,l.split(" "))
        print(letter[p-1][l][c],end="")
