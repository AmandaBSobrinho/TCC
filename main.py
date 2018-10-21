import pandas as pd
import read_signature
import peak_detection
import bootstrap
import normality_test
import confidence_interval
import pareto


def main():
    # qualitativos, quantitativos = read_signature.atribute_types()
    # print(qualitativos)
    # print(quantitativos)

    qualitativos = {'PortSrc': [1, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 6, 6, 7, 8, 8, 8, 9, 9],
                    'PortDest': [21, 21, 25, 25, 25, 25, 25, 34, 36, 40, 40, 40, 40, 89, 90]}

    quantitativos = {'nBytesSrc': [1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 5, 6, 7, 7, 8, 8, 8, 8, 8, 8, 8, 9, 9, 11, 11, 11, 11, 11, 11, 12, 12, 12,
       12, 12, 12, 13, 13, 14], 'nPortSrc': [1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 8, 8, 8, 9, 9]}

    # Atributos qualitativos
    for atributo, valores in qualitativos.items():
        atrib_freq = pareto.pareto(atributo, valores)
        print('Valores mais frequentes de ' + atributo + ': ' + ', '.join(str(valor) for valor in atrib_freq))

        # Agora tem que colocar no json


    # Para os atributos quantitativos, é preciso fazer o histograma e detectar picos
    for atributo, valores in quantitativos.items():
        histogramas = peak_detection.peak_detection(atributo, valores)
        print('\n' + atributo + ': ' + str(histogramas) + '\n')

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

            # Agora, colocar os atributos mais comuns/intervalos de confiança num json!

if __name__ == "__main__":
    main()