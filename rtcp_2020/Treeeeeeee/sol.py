import glob
import os
from PIL import Image, ImageStat
import matplotlib.pyplot as plt

if not os.path.isdir('./bigtree'):
    print("you should unzip the zip...")
else:


    print("looking for jpg...")
    files = glob.glob( './**/*.jpg', recursive=True)
    
    print("img analysis...")
    var_max = 0
    for img_name in files: 
        img = Image.open(img_name)
        stat = ImageStat.Stat(img)
        if sum(stat.var) > var_max:
            var_max = sum(stat.var)
            good_img = img_name
    
    img = Image.open(good_img)
    img.show()
    print("Flag in: ", good_img)
