# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 12:09:09 2022

@author: Yassine
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split


data_file ='training_data/training_data.csv'
model_save_path = 'keypoint_classifier.hdf5'
alldata   = np.loadtxt(data_file, delimiter=',',dtype=float)

Gestures = np.array(alldata[:,1:])

labels   = np.array(alldata[:,0], dtype='i1')


def generate_model(input_sz, num_classes):
    inputs = Input(shape=input_sz)
    L1  = Dense(300, activation = 'relu')(inputs)
    L2  = Dense(200, activation = 'relu')(L1)
    L3  = Dense(100, activation = 'relu')(L2)
    L4  = Dense(50, activation = 'relu')(L3)
    L5  = Dense(32, activation = 'relu')(L4)
    L6  = Dense(16, activation = 'relu')(L5)
    
    L7  = Dense(num_classes, activation='softmax')(L6)
        
    cnn_model = Model(inputs=inputs, outputs=L7)
        
    cnn_model.compile(loss=tf.keras.losses.categorical_crossentropy, optimizer=tf.keras.optimizers.Adam(), metrics=['accuracy'])
    cnn_model.summary()

    return cnn_model
cp_callback = tf.keras.callbacks.ModelCheckpoint(
        model_save_path, verbose=1, save_weights_only=False)  

input_size = [10]
model = generate_model(input_size, 9)


tr_gestures, ts_gestures, tr_labels, ts_labels = train_test_split(Gestures, labels, test_size=0.15, random_state=42)


tr_features = tr_gestures.reshape(-1, input_size[0], 1)
tr_labels   = to_categorical(tr_labels)

ts_features = ts_gestures.reshape(-1, input_size[0], 1)
ts_labels   = to_categorical(ts_labels)


model.fit(tr_features, tr_labels, epochs=500, callbacks=[cp_callback])

pred = model.predict(ts_features) # for induvidual gestures probablities

results = model.evaluate(ts_features, ts_labels)
print("test loss, test acc:", results)
