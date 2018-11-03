from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def pareto(titulo, data):

    freq = Counter(data)
    mostfreq = freq.most_common()

    # DataFrame para produzir as barras do gráfico
    df = pd.DataFrame(mostfreq, columns=['valores', 'freq'])

    # Obtenção das porcentagens de ocorrência de cada valor
    porcentagem = []
    for i in mostfreq:
        porcentagem.append((i[1] / len(data)) * 100)

    # Cálculo do array de porcentagens cumulativas que será usado no gráfico
    porc_pareto = np.cumsum(porcentagem)

    # Determinação dos valores que ficarão no eixo x do segundo DataFrame
    # Isso é necessário porque não dá para usar mostfreq
    x_pareto = []
    for i in mostfreq:
        x_pareto.append(i[0])

    # Obtenção do segundo DataFrame, com os valores de entrada e as porcentagens cumulativas
    df2 = pd.DataFrame({'valores': x_pareto, 'porcentagens': porc_pareto})

    # Criação do gráfico de Pareto
    # Gráfico de barras
    ax = df.groupby(['valores']).median().sort_values("freq", ascending=False).plot(kind='bar', legend=False, width=0.1)
    plt.xlabel('Valores')
    plt.ylabel('Frequências')

    # Gráfico de linha (porcentagens)
    ax2 = df2.porcentagens.plot(secondary_y='porcentagens', kind='line', ax=ax, color='C3', marker='o')
    plt.ylim(bottom=0)
    ax2.yaxis.grid()
    plt.ylabel('Porcentagens')
    plt.title('Pareto de ' + titulo)
    plt.show()

    # Determinação do retorno: valores de atributo mais frequentes
    atrib_freq = [mostfreq[0][0]]
    for i in mostfreq[1:]:  # ignora o primeiro
        if i[1] >= 0.7 * mostfreq[0][1]:  # se a frequência for maior ou igual a 70% do maior, é outro pico
            atrib_freq.append(i[0])

    # Retorna uma lista com os atributos mais frequentes
    return atrib_freq