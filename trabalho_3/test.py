#https://machinelearningmastery.com/neural-networks-are-function-approximators/#:~:text=a%20Simple%20Function-,What%20Is%20Function%20Approximation,learn%20to%20approximate%20a%20function.
#https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from numpy import asarray
from matplotlib import pyplot

# fazendo a leitura dos dados fornecidos
import csv
file = open('dados.csv')
csvreader = csv.reader(file)
# salvando as headers do csv (acho q n vamos usar pra nada)
header = []
header = next(csvreader)
# print(header)

# os valores do eixo x (Entrada) são salvos na lista entrada e os do eixo y (Saída) na lista saida
entrada = []
saida = []
for row in csvreader:
        entrada.append(row[0])
        saida.append(row[1])
print(type(entrada))
# print(entrada)

# transformando as lista em numpy.ndarrays pra manipulação ficar mais fácil
entrada = asarray(entrada)
saida = asarray(saida)
print(type(entrada))
# print(entrada)
# print(saida)

entrada = entrada.reshape((len(entrada), 1))
saida = saida.reshape((len(saida), 1))
print(type(entrada))


# separately scale the input and output variables
scale_x = MinMaxScaler()
entrada = scale_x.fit_transform(entrada)
scale_y = MinMaxScaler()
saida = scale_y.fit_transform(saida)
print(entrada.min(), entrada.max(), saida.min(), saida.max())


# design the neural network model
model = Sequential()
model.add(Dense(10, input_dim=1, activation='relu', kernel_initializer='he_uniform'))
model.add(Dense(10, activation='relu', kernel_initializer='he_uniform'))
model.add(Dense(1))

# define the loss function and optimization algorithm
model.compile(loss='mse', optimizer='adam')

# ft the model on the training dataset
model.fit(entrada, saida, epochs=100, batch_size=10, verbose=0)

# make predictions for the input data
yhat = model.predict(entrada)

x_plot = scale_x.inverse_transform(entrada)
y_plot = scale_y.inverse_transform(saida)
yhat_plot = scale_y.inverse_transform(yhat)

# report model error
print('MSE: %.3f' % mean_squared_error(saida, yhat))
# plot x vs y
pyplot.scatter(entrada,saida, label='Actual')
# plot x vs yhat
pyplot.scatter(entrada,yhat, label='Predicted')
pyplot.title('Input (x) versus Output (y)')
pyplot.xlabel('Input Variable (x)')
pyplot.ylabel('Output Variable (y)')
pyplot.legend()
pyplot.show()


