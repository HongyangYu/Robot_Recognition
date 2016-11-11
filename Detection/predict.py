from __future__ import print_function
import theano
import numpy as np
import os
import preprocess
import re
#from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from keras.models import model_from_json

batch_size = 32
trainingFile = 'training.csv'
testingCSVdir ='testingCSVs'
testingFiles = []
for filename in os.listdir(testingCSVdir):
    path = os.path.join(testingCSVdir,filename)
    testingFiles.append(path)
resultFile = 'result.csv'
architechtureFile = 'architechture.json'
weightsFile = 'weights.h5'


model = model_from_json(open(architechtureFile).read())
model.load_weights(weightsFile)
fh = open(resultFile, 'w')
fh.write('Id,Category\n')
for testingFile in testingFiles:
    test_X = preprocess.readTestingDataWindow( testingFile )    
    test_X = test_X.astype('float32')
    test_X /= 255
    test_Y = model.predict_classes(test_X, batch_size)
    result_detection, result_recognition = preprocess.organize(test_Y)
    print(result_detection)
    lines = open( testingFile, 'r' ).readlines()
    for line,result in zip(lines,result_detection):
        index = re.findall('[0-9]+', line)[-1]
        for i in range(len(result)):
            string = index+'_'+str(i+1)+','+str(int(result[i]))+'\n'
            fh.write(string)
fh.close()
        
#fh_test = open( testingFile, 'r' )
#fh_result = open( resultFile, 'w' )
#fh_result.write('Id,Category\n')
#lines = fh_test.readlines()
#print(len(lines))
#for (line,label) in zip(lines,test_Y):
#    tag = re.findall( '[0-9]+_[0-9]+',line )
#    result_string = tag[-1]+','+str(label+1)
#    fh_result.write(result_string+'\n')
#fh_result.close()
#fh_test.close()

