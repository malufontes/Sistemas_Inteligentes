from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import numpy as np
# load pima indians dataset
dataset = np.loadtxt("dadostest.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0]
Y = dataset[:,1]

X = X.reshape((len(X), 1))
Y = Y.reshape((len(Y), 1))

scale_x = MinMaxScaler()
entrada = scale_x.fit_transform(X)
scale_y = MinMaxScaler()
saida = scale_y.fit_transform(Y)

# create model
model = Sequential()
model.add(Dense(10, input_dim=1, activation='relu', kernel_initializer='he_uniform'))
model.add(Dense(10, activation='relu', kernel_initializer='he_uniform'))
model.add(Dense(1, activation='relu', kernel_initializer='he_uniform'))
# Compile model
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
# Fit the model
history = model.fit(entrada, saida, validation_split=0.30, epochs=1000, batch_size=10, verbose=0)
yhat = model.predict(entrada)
# list all data in history
print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

plt.plot(X,Y, label='Actual')
# plot x vs yhat
plt.plot(X,yhat, label='Predicted')
plt.title('Input (x) versus Output (y)')
plt.xlabel('Input Variable (x)')
plt.ylabel('Output Variable (y)')
plt.legend()
plt.show()