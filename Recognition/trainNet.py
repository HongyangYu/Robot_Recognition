from __future__ import print_function
import theano
import numpy as np
import prep
#from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils

batch_size = 32
nb_classes = 13
nb_epoch = 20
data_augmentation = True
trainingFile = 'training.csv'
testingFile = 'testing.csv'
architechtureFile = 'architechture.json'
weightsFile = 'weights.h5'
# input image dimensions
img_rows, img_cols = 40, 40
# the CIFAR10 images are RGB
img_channels = 3

#load data from local files
( X_train, y_train ) = prep.readTrainingData( trainingFile )

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
#Y_test = np_utils.to_categorical(y_test, nb_classes)

model = Sequential()

model.add(Convolution2D(32, 3, 3, border_mode='same',
                        input_shape=(img_channels, img_rows, img_cols)))
model.add(Activation('relu'))
model.add(Convolution2D(32, 3, 3))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Dense(512))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Activation('softmax'))
model.add(Activation('relu'))
model.add(Activation('relu'))
model.add(Dropout(0.25))
model.add(Convolution2D(64, 3, 3))

model.add(Convolution2D(64, 3, 3, border_mode='same'))


# let's train the model using SGD + momentum (how original).
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

X_train = X_train.astype('float32')

X_train /= 255


model.fit( X_train, Y_train, batch_size=batch_size, validation_split=0.1,\
          nb_epoch=nb_epoch, show_accuracy=True, shuffle=True )
json_string = model.to_json()
open( architechtureFile, 'w' ).write( json_string )
model.save_weights( weightsFile )
