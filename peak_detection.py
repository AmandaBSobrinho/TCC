from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def peak_detection(titulo, data):
    data.sort() # Ordenar dados de entrada

    freq = Counter(data)
    mostfreq = freq.most_common()

    df = pd.DataFrame(data, columns=['valores'])
    df.hist(histtype='step', grid=0)
    plt.title(titulo)
    plt.xlabel('Valores')
    plt.ylabel('Contagem')
    plt.show()

    moda = mostfreq[0]
    picos_iniciais = [moda]

    # Seleção inicial dos picos
    for i in mostfreq[1:]:  # ignora o primeiro
        if i[1] >= 0.7 * moda[1]:  # se a frequência for maior ou igual a 70% do maior, é outro pico
            picos_iniciais.append(i)

    # É preciso filtrar os picos pela vizinhança: só é um pico mesmo se existe um valor que não é um pico entre eles
    picos = [picos_iniciais[0]]  # o primeiro é sempre um pico
    for i in range(len(picos_iniciais) - 1):
        for j in mostfreq:
            if picos_iniciais[i][0] < j[0] < picos_iniciais[i + 1][0]:  # existe alguém que não é um pico entre os picos
                picos.append(picos_iniciais[i + 1])
                break

    entrada = np.array(data)
    histogramas = []

    if len(picos) > 1:  # se tiver mais de um pico, é preciso definir o(s) ponto(s) de corte
        corte = []
        for i in range(len(picos) - 1):
            pico1 = picos[i]
            pico2 = picos[i + 1]
            corte.append(ponto_corte(pico1, pico2, mostfreq))  # definição do(s) ponto(s) de corte

        # subdivisão do array de entrada no(s) ponto(s) de corte
        num_cortes = len(corte)

        for i in range(num_cortes):
            trecho_entrada, entrada = dividir(entrada, corte[i][0])
            histogramas.append(trecho_entrada)
        histogramas.append(entrada)

    else:  # se tiver só um pico, retorna a própria entrada
        histogramas.append(entrada)

    return histogramas


# Definindo o ponto de corte entre dois picos
def ponto_corte(pico1, pico2, mostfreq):
    corte = 100000,100000
    for i in mostfreq:
        if pico1[0] <= i[0] <= pico2[0]:
            if i[1] < corte[1]:
                corte = i
    return corte


# Divide um array em dois em um ponto de valor específico
def dividir(arr, valor):
    return arr[arr<valor], arr[~(arr<valor)]