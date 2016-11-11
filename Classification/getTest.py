from scipy.misc import imread
from scipy.misc import imsave
import os
import numpy as np

path = "test1"
img_prefix = "test_"
img_suffix = ".png"
new_prefix = "cropped_"
new_path = "/home/henry/Desktop/RobotLearning/testData1" 
#/home/henry/Desktop/RobotLearning/testData1/26_4.png
files = os.listdir( path )
test_file = 'test.csv'
test_handle = open( test_file, 'w' )
for file in files:
    if not file.endswith("txt"):
        continue
    else:
        path_join = os.path.join( path, file )
        image_name = path_join.replace( 'boxes', 'image' )
        image_name = image_name.replace( 'txt', 'png' )
        img = imread( image_name )
        file_handle = open( path_join , 'r' )
        lines = file_handle.readlines()
        for line in lines:
            data = line.split(',')
            label = data[0]
            pos = [ int(p) for p in data[1:] ]
            crop_img = img[pos[1]:pos[3], pos[0]:pos[2]]
            new_path_join = "{0}".format( label ) + img_suffix
            print new_path_join
            new_path_join = os.path.join( new_path, new_path_join )
            imsave( new_path_join , crop_img )
            test_handle.write( new_path_join + '\n' )
        file_handle.close()
test_handle.close()
