import csv

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

RANDOM_SEED = 42

dataset = 'NeuralTraining/mp-norm-coord.csv'
model_save_path = 'NeuralTraining/keypoint_classifier.hdf5'
#tflite_save_path = 'NeuralTraining/keypoint_classifier.tflite'

NUM_CLASSES = 12

X_dataset = np.loadtxt(dataset, delimiter=',', dtype='float32', usecols=list(range(1, (6 * 2) + 1)))
y_dataset = np.loadtxt(dataset, delimiter=',', dtype='int32', usecols=(0))
X_train, X_test, y_train, y_test = train_test_split(X_dataset, y_dataset, train_size=0.75, random_state=RANDOM_SEED)

model = tf.keras.models.Sequential([
    tf.keras.layers.Input((6 * 2, )),
    #tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(20, activation='relu'),
    #tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
])

cp_callback = tf.keras.callbacks.ModelCheckpoint(
    model_save_path, verbose=1, save_weights_only=False)

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
    callbacks=[cp_callback]
)
#[0.19953685998916626, 0.84449303150177, 0.1893101930618286, 0.8084837794303894, 0.17921265959739685, 0.8625568151473999, 0.1904083639383316, 0.8997052311897278, 0.2109234482049942, 0.917637825012207, 0.2852977216243744, 0.8729816675186157]
model = tf.keras.models.load_model(model_save_path)
print(X_test[0:1])
predict_result = model.predict(X_test[0:1])
print(predict_result)
print(np.squeeze(predict_result))
print(np.argmax(predict_result))
