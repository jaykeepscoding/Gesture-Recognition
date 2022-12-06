import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

dataset = 'NeuralTraining/mp-norm-coord.csv'

data = np.loadtxt(dataset, delimiter=',', dtype=float)

gestures = np.array(data[:, 1:])
labels = np.array(data[:,0], dtype='i1')

def gen_model(input_sz, num_classes):
    inputs = tf.keras.layers.Input(shape=input_sz)
    #L1 = tf.keras.layers.Dense(1000, activation='relu')(inputs)
    L1 = tf.keras.layers.Dense(600, activation='relu')(inputs)
    L2 = tf.keras.layers.Dense(300, activation='relu')(L1)
    L3 = tf.keras.layers.Dense(200, activation='relu')(L2)
    L4 = tf.keras.layers.Dense(100, activation='relu')(L3)
    L5 = tf.keras.layers.Dense(50, activation='relu')(L4)
    L6 = tf.keras.layers.Dense(32, activation='relu')(L5)
    L7 = tf.keras.layers.Dense(25, activation='relu')(L6)
    L8 = tf.keras.layers.Dense(16, activation='relu')(L7)

    L9 = tf.keras.layers.Dense(num_classes, activation='softmax')(L8)
    model = tf.keras.models.Model(inputs=inputs, outputs=L9)

    model.compile(loss=tf.keras.losses.categorical_crossentropy, optimizer='Adam', metrics=['accuracy'])
    model.summary()

    return model

model = gen_model(12, 9)

train_gestures, test_gestures, train_labels, test_labels = train_test_split(gestures, labels, test_size=0.15, random_state=42)

train_features = train_gestures.reshape(-1, 12, 1)
train_labels = tf.keras.utils.to_categorical(train_labels)

test_features = test_gestures.reshape(-1, 12, 1)
test_labels = tf.keras.utils.to_categorical(test_labels)

model.fit(train_features, train_labels, epochs=500)

pred = model.predict(test_features)

results = model.evaluate(test_features, test_labels)
print("test loss, test acc: ", results)