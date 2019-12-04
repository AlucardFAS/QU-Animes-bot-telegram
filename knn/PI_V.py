import csv
import sys
import math
import random
import operator

#Carrega o arquivo CSV
def load_data(filename):
    with open(filename, 'r') as csvfile:#Carrega como CSV File
        lines = csv.reader(csvfile)#Armazena os valores em linhas
        dataset = list(lines)#Cria uma lista
        return dataset

#Acha vizinhos
#Recebe os conjuntos, sendo um de treino onde estão os dados com as classes, um de teste,
#onde estão as instâncias sem a classe(que você quer saber os vizinhos mais próximos),
#e o numero k de vizinhos a serem investigados.
def getVizinhos(conjuntoTratado, instanciaTeste, k):
	distancia = []
	length = len(instanciaTeste)-1#porque é um vetor

    #Fará o calculo euclidiano de distancia entre os n valores teste 
	for x in range(len(conjuntoTratado)):
		dist = distanciaEuclidiana(instanciaTeste, conjuntoTratado[x], length)
		distancia.append((conjuntoTratado[x], dist))
	distancia.sort(key=operator.itemgetter(1))#Ordena o vetor de distancia['valores', distancia] pela distancia
	vizinhos = []
	for x in range(int(k)):
		vizinhos.append(distancia[x][0])#para o numero k de vizinhos, varre a lista e obtém as instancias de vizinhos
	return vizinhos

#Divisão segura para o caso ZERO
def divisaoSegura(x, y):
    return 0 if y == 0 else x / y

#calculo de distancia eucliadiana
def distanciaEuclidiana(instancia1, instancia2, length):
	distancia = 0
	for x in range(1, length):
		distancia += pow((instancia1[x] - instancia2[x]), 2)
	return math.sqrt(distancia)

#Define a classe tendo como base os vizinhos
def getResposta(vizinhos):
	classeVotos = {}#Cria um Dict(Tipo um JSON)
	for x in range(len(vizinhos)):#le ate o ultimo vizinho
		resposta = vizinhos[x][-1]#armazena de cada linha o ultimo valor
		if resposta in classeVotos:#se o valor armazenado pertence a um dict, incrementa esse valor
			classeVotos[resposta] += 1
		else:#senão, cria um novo dict e define que existe 1 instancia
			classeVotos[resposta] = 1
	votosOrdenados = sorted(classeVotos.items(), key=operator.itemgetter(1), reverse=True)# Ordena os valores do maior pro menor
	return votosOrdenados[0][0]

def runKnnOnDataset(input_to_knn, num_recomendations):
    data = load_data('.\data\dataset-output.csv')
    for x in range (len(data)):
        for y in range(11):
            data[x][y] = float(data[x][y])

    get_recomendation(data, 11, input_to_knn, num_recomendations)

def get_recomendation(dataset, columns, similar, num_recomendations):
    dados = getVizinhos(dataaset, similar, num_recomendations)
    print(dados)


runKnnOnDataset([10,1,20,29,8,11,22,3,2,2,1,12], 2)