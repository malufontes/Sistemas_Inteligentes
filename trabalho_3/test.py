# fazendo a leitura dos dados fornecidos
import csv
file = open('dados.csv')
csvreader = csv.reader(file)
# salvando as headers do csv (acho q n vamos usar pra nada)
header = []
header = next(csvreader)
# print(header)

# os valores do eixo x (Entrada) são salvos no array entrada e os do eixo y (Saída) noarray saida
entrada = []
saida = []
for row in csvreader:
        entrada.append(row[0])
        saida.append(row[1])
