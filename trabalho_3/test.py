#https://machinelearningmastery.com/neural-networks-are-function-approximators/#:~:text=a%20Simple%20Function-,What%20Is%20Function%20Approximation,learn%20to%20approximate%20a%20function.
#https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/

#history
#https://machinelearningmastery.com/display-deep-learning-model-training-history-in-keras/

from __future__ import print_function
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
# print(type(entrada))
# print(entrada)

# transformando as lista em numpy.ndarrays pra manipulação ficar mais fácil
entrada = asarray(entrada)
saida = asarray(saida)
# print(type(entrada))
# print(entrada)
# print(saida)

entrada = entrada.reshape((len(entrada), 1))
saida = saida.reshape((len(saida), 1))
# print(type(entrada))


# separately scale the input and output variables
scale_x = MinMaxScaler()
entrada = scale_x.fit_transform(entrada)
scale_y = MinMaxScaler()
saida = scale_y.fit_transform(saida)
# print(entrada.min(), entrada.max(), saida.min(), saida.max())


# design the neural network model
model = Sequential()
model.add(Dense(10, input_dim=1, activation='relu', kernel_initializer='he_uniform'))
model.add(Dense(10, activation='relu', kernel_initializer='he_uniform'))
model.add(Dense(1))

# define the loss function and optimization algorithm
model.compile(loss='mse', optimizer='adam')

# ft the model on the training dataset
history = model.fit(entrada, saida, validation_split=0.15, epochs=3000, batch_size=10, verbose=0)

# make predictions for the input data   

ypredict = model.predict(entrada)

x_plot = scale_x.inverse_transform(entrada)
y_plot = scale_y.inverse_transform(saida)
ypredict_plot = scale_y.inverse_transform(ypredict)

# report model error
print('MSE: %.3f' % mean_squared_error(saida, ypredict))

fig, axs = pyplot.subplots(1, 2)

# plot x vs real y
axs[0].plot(x_plot,y_plot, label='Actual', color = 'b')
# plot x vs ypredict
axs[0].plot(x_plot,ypredict_plot, label='Predicted', color = 'tab:orange')
axs[0].set_title('Input (x) versus Output (y)')
axs[0].set(xlabel='Input Variable (x)', ylabel='Output Variable (y)')
axs[0].legend()
axs[0].label_outer()

#plot loss
axs[1].plot(history.history['val_loss'], color = 'tab:orange')
axs[1].set_title('model loss')
axs[1].set(xlabel='epoch', ylabel='loss')
axs[1].yaxis.set_label_position("right")
axs[1].yaxis.tick_right()
axs[1].label_outer()


pyplot.savefig('plot.png')
pyplot.show()

terminalinput = "0"

while(terminalinput != ""):
        terminalinput = input("Digite valor dentro do intervalo ou Enter para sair: ") 
        if(terminalinput == ""):
                break
        terminalinput = int(terminalinput)
        if(terminalinput % 1 != 0 or terminalinput<0 or terminalinput>60):
                print("número inválido")
                break

        print("número: " + str(terminalinput))
        print("y real->", end = ''); print(y_plot[terminalinput])
        print("y est ->", end = ''); print(ypredict_plot[terminalinput])

        x=9
        if(terminalinput<9):
                x=terminalinput

        x_partial = x_plot[terminalinput-x:terminalinput+10]
        y_partial = y_plot[terminalinput-x:terminalinput+10]
        ypredict_partial = ypredict_plot[terminalinput-x:terminalinput+10]

        pyplot.plot(x_partial,y_partial, label='Actual', color = 'b')
        pyplot.plot(x_partial,ypredict_partial, label='Predicted', color = 'tab:orange')

        pyplot.plot(terminalinput,y_plot[terminalinput], 'ro')
        pyplot.plot(terminalinput,ypredict_plot[terminalinput], 'ro')

        pyplot.title('Partial Input (x) versus Output (y)')
        pyplot.xlabel('Input Variable (x)')
        pyplot.ylabel('Output Variable (y)')
        pyplot.legend()

        pyplot.show()