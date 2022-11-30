import csv

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

RANDOM_SEED = 42

dataset = 'NeuralTraining/mp-norm-coord.csv'
model_save_path = 'NeuralTraining/keypoint_classifier.hdf5'
#tflite_save_path = 'NeuralTraining/keypoint_classifier.tflite'

NUM_CLASSES = 8

X_dataset = np.loadtxt(dataset, delimiter=',', dtype='float32', usecols=list(range(1, (6 * 2) + 1)))
y_dataset = np.loadtxt(dataset, delimiter=',', dtype='int32', usecols=(0))
X_train, X_test, y_train, y_test = train_test_split(X_dataset, y_dataset, train_size=0.75, random_state=RANDOM_SEED)

model = tf.keras.models.Sequential([
    #tf.keras.layers.Input((6 * 2, )),
    #tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(20, activation='relu'),
    #tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(
    X_train,
    y_train,
    epochs=1000,
    batch_size=128,
    validation_data=(X_test, y_test),
    #callbacks=[cp_callback, es_callback]
)

model = tf.keras.models.load_model(model_save_path)