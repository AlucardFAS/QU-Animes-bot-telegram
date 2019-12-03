import csv
import sys
import math
import random
import operator

#Carrega o arquivo CSV
def carregaDados(filename):
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
	for x in range(length):
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

def runKnnOnDataset():
    data = carregaDados('.\data\dataset-output.csv')
    dataM = [[]]
    for x in range (len(data)):
        for y in range(11):
            dataM[x][y] = float(data[x][y])

    print()
    fazCaralhadaDeCoisaRever(dataM,15,15,48842,1)
    print()
    print()

def preparaDataset(dataset, conjuntoTratado, conjuntoTeste,amostra,amostraInicial,coluna):
    for x in range(len(dataset)):
            for y in range(coluna):#le os n elementos de cada linha
                dataset[x][y] = float(dataset[x][y])#Gera uma matriz de elementos do dataset

            if (x >= (amostra - amostraInicial)) & (x < amostra):
                    conjuntoTeste.append(dataset[x])
            else:
                    conjuntoTratado.append(dataset[x])
                   
def multiclasses(pontosAcertados,pontosErrados):
    precisao = acuracia = 0
    for x in (range(0,10)):
        precisao += (pontosAcertados/(pontosAcertados + pontosErrados))*10
        acuracia = precisao/10

    return acuracia

def fazCaralhadaDeCoisaRever(dataset,coluna,m,linhas,tipoclasse):
    
    amostra = int(linhas/10)
    amostraInicial = amostra
    trainingSet = []
    testSet = []
    acerto = erro = acertom2 = errom2 = acertom10 = errom10 = acertoqnn = erroqnn = erroCruzadov1nn = mediav1nn = erroCruzadom2 = erroCruzadom10 = erroCruzadoqnn = 0
    acuracia = acuraciam2 = acuraciam10 = acuraciaqnn = tp = fp = tn = fn = tp2 = fp2 = tn2 = fn2 = tp10 = fp10 = tn10 = fn10 = tpnn = fpnn = tnnn = fnnn = sensibilidade = especificidade = precisaoBinaria = revocacao = 0
    sensibilidade2 = especificidade2 = precisaoBinaria2 = revocacao2 = sensibilidade10 = especificidade10 = precisaoBinaria10 = revocacao10 = sensibilidadenn = especificidadenn = precisaoBinariann = revocacaonn = 0
    i = 0
    for x in (range(0,10)):
       i+=1
       preparaDataset(dataset,trainingSet,testSet,amostra,amostraInicial,coluna)
       amostra+=amostraInicial   

       for y in (range(0,len(testSet))):
           
           #v1nn
           v1nn = getVizinhos(trainingSet,testSet[y],1)
           result = (getResposta(v1nn))
           atual = (testSet[y][-1])

           #m2nn
           m2nn = getVizinhos(trainingSet,testSet[y],m+2)
           resultm2 = getResposta(m2nn)
           atualm2 = testSet[y][-1]

           #m10nn
           m10 = getVizinhos(trainingSet,testSet[y],m*10+1)
           resultm10 = getResposta(m2nn)
           atualm10 = testSet[y][-1]



def main():
    runKnnOnDataset()

main()
