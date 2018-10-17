import pandas as pd
import matplotlib.pyplot as plt


def bootstrap(titulo, data):
    df = pd.DataFrame(data, columns=['valores'])
    new_bootstrap = pd.DataFrame({'meangrade': [df.sample(10, replace=True).valores.mean() for i in range(1000)]})

    new_bootstrap.meangrade.hist(histtype='step', grid=0)
    plt.axvline(df.valores.mean(), color='C1')
    plt.title(titulo + ' Bootstrapped')
    plt.xlabel('Valores')
    plt.ylabel('Contagem')
    plt.show()

    min_quantile = new_bootstrap.meangrade.quantile(0.025)
    max_quantile = new_bootstrap.meangrade.quantile(0.975)

    return new_bootstrap, round(min_quantile), round(max_quantile)
