import pandas as pd
import matplotlib.pyplot as plt


def bootstrap(titulo, data):
    df = pd.DataFrame(data, columns=['valores'])
    new_bootstrap = pd.DataFrame({'meangrade': [df.sample(100, replace=True).valores.mean() for i in range(1000)]})

    new_bootstrap.meangrade.hist(histtype='step', grid=0)
    plt.axvline(df.valores.mean(), color='C1')
    plt.title(titulo + ' Bootstrapped')
    plt.xlabel('Valores')
    plt.ylabel('Contagem')
    plt.show()

    return new_bootstrap
