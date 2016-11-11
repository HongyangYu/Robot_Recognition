from __future__ import print_function
import theano
import preprocess
import re
import numpy as np
from keras.optimizers import SGD
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.convolutional import Convolution2D, MaxPooling2D

batch_size = 32
train_file = 'train.csv'
test_file = 'test.csv'
result_file = 'result.csv'
arch_file = 'architechture.json'
weight_file = 'weight.h5'
 

test_X = preprocess.readTest( test_file )
test_X = test_X.astype('float32')
test_X /= 255
model = model_from_json(open(arch_file).read())
model.load_weights(weight_file)
test_Y = model.predict_classes(test_X, batch_size)
# print(test_Y)
test_handle = open( test_file, 'r' )
result_handle = open( result_file, 'w' )
result_handle.write('Id,Category\n')
lines = test_handle.readlines()
# print(len(lines))
for (line,label) in zip(lines,test_Y):
    tag = re.findall( '[0-9]+_[0-9]+',line )
    result_string = tag[-1]+','+str(label+1)
    result_handle.write(result_string+'\n')
result_handle.close()
test_handle.close()

