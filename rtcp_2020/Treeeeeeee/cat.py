from PIL import Image

def hex_to_rgb(hex):
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

with open("hint.txt","r") as f:
    lines = f.readlines()[0][:-1].split(" ")

colors = []
for line in lines:
    line=line.split("#")[1:]
    colors.append(line)

col = len(colors[0])
row = len(colors)
im = Image.new("RGB", (col,row), color = (0,255,255))

pixels=im.load()

for i in range(im.size[0]): # for every pixel:
    for j in range(im.size[1]):
        pixels[i,j] = hex_to_rgb(colors[j][i])
print("saving picture of a cat!")
im.save("cat.png")

