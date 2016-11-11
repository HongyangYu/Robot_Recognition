import cv2
import os
import numpy as np

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
        path_join = os.path.join( path, file )
        image_name = path_join.replace( 'boxes', 'image' )
        image_name = image_name.replace( 'txt', 'png' )
        img = cv2.imread( image_name )
        file_handle = open( path_join , 'r' )
        lines = file_handle.readlines()
        for line in lines:
            data = line.split(',')
            label = data[0]
            pos = [ int(p) for p in data[1:] ]
            crop_img = img[pos[1]:pos[3], pos[0]:pos[2]]
            names[label] = names.get(label,0) + 1
            new_path = 'training{0}'.format(label)
            new_path_join = new_prefix + "{0}_{1}".format( label, str(names[label])) + img_suffix
            new_path_join = os.path.join( new_path, new_path_join )
            cv2.imwrite( new_path_join , crop_img )
        file_handle.close()