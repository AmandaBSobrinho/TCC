import pandas as pd
import read_signature
import read_each_signature
import peak_detection
import bootstrap
import normality_test
import confidence_interval
import pareto
import json
import os
from shutil import copy2


def main():
    sig_path = input("Caminho das assinaturas (com barra no final): ")
    # sig_path = '/home/amanda/PycharmProjects/TCC/Signatures/'
    qualitativos, quantitativos = read_signature.atribute_types(sig_path)
    print('Qualitativos: ' + str(qualitativos))
    print('\nQuantitativos:' + str(quantitativos))

    # qualitativos = {'PortSrc': [1, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 6, 6, 7, 8, 8, 8, 9, 9],
    #                 'PortDest': [21, 21, 25, 25, 25, 25, 25, 34, 36, 40, 40, 40, 40, 89, 90]}

    # quantitativos = {'nBytesSrc': [1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 5, 6, 7, 7, 8, 8, 8, 8, 8, 8, 8, 9, 9, 11, 11, 11, 11, 11, 11, 12, 12, 12,
    #    12, 12, 12, 13, 13, 14], 'nPortSrc': [1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 8, 8, 8, 9, 9]}

    saida_json = {}

    # Atributos qualitativos
    for atributo, valores in qualitativos.items():
        atrib_freq = pareto.pareto(atributo, valores)
        print('\nValores mais frequentes de ' + atributo + ': ' + ', '.join(str(valor) for valor in atrib_freq))

        saida_json[atributo] = {}  # Criação do dicionário do atributo
        saida_json[atributo].update({"tipo": 'qualitativo'})
        saida_json[atributo].update({"valor": atrib_freq})  # Atualiza o dicionário com um novo atributo e seu valor

    # Para os atributos quantitativos, é preciso fazer o histograma e detectar picos
    for atributo, valores in quantitativos.items():
        histogramas = peak_detection.peak_detection(atributo, valores)
        print('\n' + atributo + ': ' + str(histogramas) + '\n')

        saida_json[atributo] = {}  # Criação do dicionário do atributo
        saida_json[atributo].update({"tipo": 'quantitativo'})
        cont = 1  # Contador para escrever a chave valor consecutivamente

        for histograma in histogramas:

            # Primeiro tem o teste de normalidade. Se já for uma normal, não precisa do bootstrap
            # if normality_test.normality(histograma):
            #     print('Dados de entrada sao normais!')
            #     saida_normalizada = pd.DataFrame(histograma, columns=['valores'])
            #
            # else:
            #     # Senão, faz o bootstrap
            #     print('Dados de entrada não são normais!')

            # Bootstrap (sem teste de normalidade)
            saida_normalizada = bootstrap.bootstrap(atributo, histograma)

            # Cálculo do intervalo de confiança
            min_quantile, max_quantile = confidence_interval.calculate(saida_normalizada)
            print('Intervalo de confiança de ' + atributo + ': ' + str(min_quantile) + ' - ' + str(max_quantile))

            # Atualiza a chave atributo com um novo par de valores min e max
            saida_json[atributo].update({'valor{}'.format(cont): [min_quantile, max_quantile]})
            cont = cont + 1

    # Se o arquivo já existe, apaga e cria outro
    if os.path.exists('valores.json'):
        os.remove('valores.json')
    with open('valores.json', 'a') as arquivo:
        json.dump(saida_json, arquivo, indent=4)

    print('\n\n--VERIFICAÇÃO DAS ASSINATURAS--\n')
    # Agora, precisa caminhar pelo json enquanto analisa as assinaturas para definir quais são melhores
    # Pega todas as assinaturas dentro da pasta
    files = [os.path.join(sig_path, f) for f in os.listdir(sig_path) if os.path.isfile(os.path.join(sig_path, f))]

    # Pede o nome da pasta em que as assinaturas classificadas vão ficar
    class_signatures_name = input('\nNome da pasta das Assinaturas Classificadas: ')
    class_signatures_path = os.getcwd() + '/' + class_signatures_name + '/'
    if not os.path.exists(class_signatures_path):  # Se a pasta não existe, criar
        os.makedirs(class_signatures_path)

    for file in files:
        print('\n\nAssinatura: ' + str(file))
        # Guarda cada valor de cada atributo de cada assinatura em dois dicionários
        qualitativos_sig, quantitativos_sig, number_atrib_total = read_each_signature.read_atributes(file)
        number_atrib = 0

        # Para cada atributo qualitativo, verifica se o valor naquela assinatura é algum dos valores em saida_json
        for atrib_name, atrib_value in qualitativos_sig.items():
            for i in saida_json[atrib_name]['valor']:
                if atrib_value == i:
                    print('\nAtributo qualitativo ' + atrib_name + ' tem valor ' + str(atrib_value))
                    number_atrib = number_atrib + 1  # Soma um no total de atributos que têm o valor estabelecido
                    break

        # Para cada atributo quantitativo, verifica se o valor naquela assinatura está em algum dos intervalos
        for atrib_name, atrib_value in quantitativos_sig.items():
            for i in range(1,len(saida_json[atrib_name])):
                if saida_json[atrib_name]['valor{}'.format(i)][0] <= atrib_value <= saida_json[atrib_name]['valor{}'.format(i)][1]:
                    print('\nAtributo quantitativo ' + atrib_name + ' tem valor ' + str(atrib_value))
                    number_atrib = number_atrib + 1  # Soma um no total de atributos que têm valor no intevalo
                    break

        sig_class = (number_atrib/number_atrib_total)*100  # Calcula a classificação da assinatura
        print('\nClassificação: ' + str(sig_class))

        # Copia a assinatura para alguma das pastas
        intervals = [[0,10], [10,20], [20,30], [30,40], [40,50], [50,60], [60,70], [70,80], [80,90], [90,100]]

        for i in intervals:
            if i[0] < sig_class <= i[1]:
                # Copiar para aquela pasta
                # Criar pasta, se ela não existe
                directory = class_signatures_path + str(i[0]) + '-' + str(i[1]) + '/'
                if not os.path.exists(directory):  # Se a pasta não existe, criar
                    os.makedirs(directory)
                copy2(file, directory + os.path.relpath(file, sig_path))

            # Caso a classificação seja zero
            if sig_class == 0:
                directory = class_signatures_path + '0/'
                if not os.path.exists(directory):  # Se a pasta não existe, criar
                    os.makedirs(directory)
                copy2(file, directory + os.path.relpath(file, sig_path))


if __name__ == "__main__":
    main()