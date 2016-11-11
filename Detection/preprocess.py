# include basic functions used to preprocess images
import numpy as np
from scipy.misc import imresize
from scipy.misc import imread

seperator =  ';'
def readTrain( filename ):
    data_X = []
    data_Y = []    
    file_handle = open( filename, 'r' )
    lines = file_handle.readlines()
    for line in lines:
        ele = line.split(seperator)
        data = imread( ele[0] )
		data = imresize( data, (50, 50) )
        data_X.append(data)
        data_Y.append([int( ele[1] )])
    X = np.array(data_X)
    Y = np.array(data_Y)
    X = np.swapaxes(X, 2, 3) //@@
    X = np.swapaxes(X, 1, 2) 
    return X, Y
def readTest( filename ):
    data_X = []    
    file_handle = open( filename, 'r' )
    lines = file_handle.readlines()
    for line in lines:
        image_name = line.rstrip()
        data = imread( image_name )
        data = imresize( data, (50, 50) )     
        data_X.append(data)
    X = np.array(data_X)
    X = np.swapaxes(X, 2, 3)
    X = np.swapaxes(X, 1, 2) 
    return X
