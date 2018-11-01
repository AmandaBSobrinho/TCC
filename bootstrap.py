import pandas as pd
import matplotlib.pyplot as plt


def bootstrap(titulo, data):
    df = pd.DataFrame(data, columns=['entradas'])
    new_bootstrap = pd.DataFrame({'valores': [df.sample(100, replace=True).entradas.mean() for i in range(1000)]})

    new_bootstrap.valores.hist(histtype='step', grid=0)
    plt.axvline(df.entradas.mean(), color='C1')
    plt.title(titulo + ' Bootstrapped')
    plt.xlabel('Valores')
    plt.ylabel('Contagem')
    plt.show()

    # min_quantile = new_bootstrap.valores.quantile(0.025)
    # max_quantile = new_bootstrap.valores.quantile(0.975)

    return new_bootstrap
