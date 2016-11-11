# include basic functions used to preprocess images
import numpy as np
from scipy.misc import imresize
from scipy.misc import imread
from scipy.misc import imshow

img_row, img_col = 40, 40
w_height,w_width = 120,120
ratio_ = float(img_row)/w_height
window_step = 30
img_height, img_width = 400,640
ratio = 1
seperator =  ';'
windows_x = range(0,int(img_width*ratio)-w_width+1,window_step)
windows_y = range(0,int(img_height*ratio)-w_height+1,window_step)
windows = []
for y in windows_y:
    for x in windows_x:
        windows.append([(x,y),(x+w_width-1,y+w_height-1)])


def resizeimage( img ):
    croppedimg = imresize( img, (img_row, img_col) )
    return croppedimg
def readTrainingData( filename ):
    fh = open( filename, 'r' )
    lines = fh.readlines()
    data_X = []
    data_Y = []    
    for line in lines:
        items = line.split(seperator)
        data = imread( items[0] )
        data = resizeimage( data )       
        label = [int( items[1] )]
        data_X.append(data)
        data_Y.append(label)
    X = np.array(data_X)
    Y = np.array(data_Y)
    X = np.swapaxes(X, 2, 3)
    X = np.swapaxes(X, 1, 2) 
    return X, Y
def readTestingData( filename ):
    fh = open( filename, 'r' )
    lines = fh.readlines()
    data_X = []    
    for line in lines:
        imgName = line.rstrip()
        data = imread( imgName )
        data = resizeimage( data )       
        data_X.append(data)
    X = np.array(data_X)
    X = np.swapaxes(X, 2, 3)
    X = np.swapaxes(X, 1, 2) 
    return X
def readTestingDataWindow( filename ):
    fh = open( filename, 'r' )
    lines = fh.readlines()
    if len(lines)<1:
        return None
    data_X = []
    for line in lines:
        imgName = line.rstrip()
        data = imread( imgName )
        if(len(data)==0):
            print line
        #data = imresize( data, ratio )
        img_stack = stackImage(data)
        data_X += img_stack
    X = np.array(data_X)
    X = np.swapaxes(X, 2, 3)
    X = np.swapaxes(X, 1, 2)
    return X
def stackImage(data):
    img_stack = []    
    for window in windows:
        x1 = window[0][0]
        x2 = window[1][0]
        y1 = window[0][1]
        y2 = window[1][1]
        newimg = imresize(data[y1:y2,x1:x2],(img_row,img_col))
        img_stack.append(newimg)
        #imshow(newimg)
    return img_stack
def organize(labels):
    num_file = len(labels)/len(windows)
    detection = []
    recognition = []
    labels = (labels+1)%13
    x = len(windows_x)
    y = len(windows_y)
    img = np.empty((y,x))
    k = 0;
    detections = []
    boundingBoxes = []
    boxes = {}
    for i in range(num_file):
        classes = [0]*12
        coord = {}
        for row in range(y):
            for col in range(x):
                val = labels[k]
                img[row][col] = val
                k += 1
                if val>0:
                    classes[val-1] += 1
        for row in range(1,y-1):
            for col in range(1,x-1):
                val =int(img[row][col])
                val_1 = int(img[row-1][col])
                val_2 = int(img[row][col-1])
                val_3 = int(img[row][col+1])
                val_4 = int(img[row+1][col])
                if val > 0 and (val_1 == val or val_2 == val or val_3 == val or val_4 == val):
                    classes[val-1] += 2
                    boxes[val-1] = boxes.get(val-1,[])+[(row,col)]
        boundingBox = {}        
        for key,coord in boxes.items():
            y = coord[-1][0]
            x = coord[-1][1]
            boundingBox[key] = boundingBox.get(key,[])+[x*window_step, y*window_step,\
                                                        x*window_step+w_width, y*window_step+w_height]
        boundingBoxes.append(boundingBox)
        detection = [val >= 1 for val in classes]
        detections.append(detection)
    return detections,boundingBoxes
