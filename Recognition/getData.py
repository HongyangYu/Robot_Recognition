from scipy.misc import imread
from scipy.misc import imsave
import numpy as np
import os

path = "train"
img_prefix = "image_"
img_suffix = ".png"
new_prefix = "cropped_"
files = os.listdir( path )
names = {}
for file in files:
    if not file.endswith("txt"):
        continue
    else:
        txtFilename = os.path.join( path, file )
        imgName = txtFilename.replace( 'boxes', 'image' )
        imgName = imgName.replace( 'txt', 'png' )
        img = imread( imgName )
        fh = open( txtFilename , 'r' )
        lines = fh.readlines()
        if len(lines) < 1:
            continue
        for line in lines:
            data = line.split(',')
            label = data[0]
            pos = [ int(p) for p in data[1:] ]
            crop_img = img[pos[1]:pos[3], pos[0]:pos[2]]
            names[label] = names.get(label,0) + 1
            newPath = 'trainData/training{0}'.format(label)
            newFilename = new_prefix + "{0}_{1}".format( label, str(names[label])) + img_suffix
            newFilename = os.path.join( newPath, newFilename )
            imsave( newFilename , crop_img )
        fh.close()
