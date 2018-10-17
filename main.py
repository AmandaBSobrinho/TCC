import read_signature
import peak_detection
import bootstrap

def main():
    # qualitativos, quantitativos = read_signature.atribute_types()
    # print(qualitativos)
    # print(quantitativos)

    quantitativos = {'nBytesSrc': [1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 5, 6, 7, 7, 8, 8, 8, 8, 8, 8, 8, 9, 9, 11, 11, 11, 11, 11, 11, 12, 12, 12,
       12, 12, 12, 13, 13, 14], 'nPortSrc': [1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 8, 8, 8, 9, 9]}

    # Para os atributos quantitativos, é preciso fazer o histograma e detectar picos
    for atributo, valores in quantitativos.items():
        histogramas = peak_detection.peak_detection(atributo, valores)
        print(atributo + ': ' + str(histogramas))
        for histograma in histogramas:
            # Primeiro tem o teste de normalidade. Se já for uma normal, não precisa do bootstrap
            # Senão, faz o bootstrap
            bootstrapped, min_quantile, max_quantile = bootstrap.bootstrap(atributo, histograma)
            print('Intervalo de confiança de ' + atributo + ': ' + str(min_quantile) + ' - ' + str(max_quantile))


if __name__ == "__main__":
    main()