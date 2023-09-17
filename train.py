import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
data = pd.read_csv('dataset/Super_Snake.csv')
data.fillna(0, inplace=True)
X = data.iloc[:, :-1].values 
Y = data.iloc[:, -1].values  
learning_rate =0.002
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(12, activation='relu'),
    tf.keras.layers.Dense(50, activation='relu'),
    tf.keras.layers.Dense(30, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax')
])
model.compile(optimizer='adam',
              loss= tf.keras.losses.sparse_categorical_crossentropy,
              metrics=['accuracy'])
output = model.fit(X_train, Y_train, epochs=200)
loss, accuracy = model.evaluate(X_test, Y_test)
print("loss test:" , loss)
print("accuracy test:" ,accuracy)   
model.save('weights/SuperSnake.h5')