# -*- coding: utf-8 -*-
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
import os

# Any results you write to the current directory are saved as output.

"""### **Importing libraries**"""
#import non tensorflow libraries
import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image
import pathlib
# import IPython.display as display

#import tensorflow libraries
import tensorflow as tf
from tensorflow import keras
from keras._tf_keras.keras.preprocessing.image import ImageDataGenerator

"""## **Data Preparation**"""

# data_dir = 'dataset/images'
data_dir = 'dataset/test_images'  # for toy dataset
templates = 'templates.txt'

#initialise class names and view them
# with open(templates, "r") as f:
#     CLASS_NAMES = [item.strip() for item in f]
# CLASS_NAMES = np.array(CLASS_NAMES)
# print(len(CLASS_NAMES))

CLASS_NAMES = np.array(["book", "dog"])  # toy dataset of just cats and dogs


#initialising necessary properties
BATCH_SIZE = 32
IMG_HEIGHT = 224
IMG_WIDTH = 224
STEPS_PER_EPOCH = np.ceil(10000/BATCH_SIZE)

#prepare train data generator with necessary augmentations and validation split
train_datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        rescale=1./255,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.25)

#initialise train directory
data_dir = pathlib.Path(data_dir)

#generate training data
print('Train Data')
train_data = train_datagen.flow_from_directory(
    str(data_dir),
    batch_size=BATCH_SIZE,
    shuffle=True,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    classes = list(CLASS_NAMES),
    subset='training')

#generate validation data
print('\nValidation Data')
valid_data = train_datagen.flow_from_directory(
    str(data_dir),
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    subset='validation')

#vizualise the loaded images
def show_batch(image_batch, label_batch):
  fig = plt.figure(figsize=(10,10))
  fig.patch.set_facecolor('white')
  for n in range(25):
      ax = plt.subplot(5,5,n+1)
      plt.imshow(image_batch[n])
      plt.title(CLASS_NAMES[label_batch[n]==1][0].title(), fontsize=14)
      plt.axis('off')
image_batch, label_batch = next(train_data)
# show_batch(image_batch, label_batch)

"""## **MobileNetV2**

Fine Tuning the model by adding extra classification layers and training the entire models with imagenet weights.
"""

#import model
# from tensorflow.keras.applications import MobileNetV2

#initialise base model
IMG_SHAPE = (IMG_HEIGHT, IMG_WIDTH, 3)
base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE, input_tensor=None,
                                                include_top=False,
                                                weights='imagenet')
base_model.trainable = True

#define model
model = tf.keras.Sequential()
model.add(base_model)
model.add(tf.keras.layers.GlobalAveragePooling2D())
model.add(tf.keras.layers.Dense(320, activation='relu'))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(320, activation='relu'))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(len(CLASS_NAMES), activation='softmax'))  # had to change this to be the shape of the number of classes
#compile model
model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.001, momentum=0.9),
      loss = tf.keras.losses.CategoricalCrossentropy(from_logits = True),
      metrics=['accuracy'])
print(model.summary())

epochs = 5

# Reduce learning rate when there is a change lesser than <min_delta> in <val_accuracy> for more than <patience> epochs
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor = 'val_accuracy',
                                                 mode = 'max',
                                                 min_delta = 0.01,
                                                 patience = 3,
                                                 factor = 0.25,
                                                 verbose = 1,
                                                 cooldown = 0,
                                                 min_lr = 0.00000001)

# Stop the training process when there is a change lesser than <min_delta> in <val_accuracy> for more than <patience> epochs
early_stopper = tf.keras.callbacks.EarlyStopping(monitor = 'val_accuracy',
                                                 mode = 'max',
                                                 min_delta = 0.005,
                                                 patience = 10,
                                                 verbose = 1,
                                                 restore_best_weights = True)
#fit the model
history = model.fit(train_data,
                    epochs=epochs,
                    validation_data = valid_data,
                    callbacks=[early_stopper, reduce_lr])

#get results
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

#plot results
#accuracy
plt.figure(figsize=(8, 8))
plt.rcParams['figure.figsize'] = [16, 9]
plt.rcParams['font.size'] = 14
plt.rcParams['axes.grid'] = True
plt.rcParams['figure.facecolor'] = 'white'
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
plt.title(f'MobileNetV2 \nTraining and Validation Accuracy. \nTrain Accuracy: {str(acc[-1])}\nValidation Accuracy: {str(val_acc[-1])}')

#loss
plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.ylabel('Cross Entropy')
plt.title(f'Training and Validation Loss. \nTrain Loss: {str(loss[-1])}\nValidation Loss: {str(val_loss[-1])}')
plt.xlabel('epoch')
plt.tight_layout(pad=3.0)
plt.show()