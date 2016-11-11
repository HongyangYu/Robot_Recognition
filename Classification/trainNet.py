from __future__ import print_function
import theano
import preprocess
import numpy as np
from keras.models import Sequential
from keras.optimizers import SGD
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D

batch_size = 50
nb_classes = 12
nb_epoch = 50
data_augmentation = True
train_file = 'train.csv'
test_file = 'test.csv'
arch_file = 'architechture.json'
weightsFile = 'weight.h5'
# input image dimensions
img_rows, img_cols = 50, 50
# the CIFAR10 images are RGB
img_channels = 3

#load data from local files
( X_train, y_train ) = preprocess.readTrain( train_file )

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
#Y_test = np_utils.to_categorical(y_test, nb_classes)

model = Sequential()

model.add(Convolution2D(32, 3, 3, border_mode='same',
                        input_shape=(img_channels, img_rows, img_cols)))
model.add(Activation('relu'))
model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Convolution2D(64, 3, 3, border_mode='same'))
model.add(Activation('relu'))
model.add(Convolution2D(64, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

# let's train the model using SGD + momentum (how original).
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

X_train = X_train.astype('float32')

X_train /= 255


model.fit( X_train, Y_train, batch_size=batch_size,
          nb_epoch=nb_epoch, show_accuracy=True, shuffle=True )
json_string = model.to_json()
open( arch_file, 'w' ).write( json_string )
model.save_weights( weightsFile )
