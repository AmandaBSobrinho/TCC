def calculate(dataframe):

    # Cálculo do intervalo de confiança
    min_quantile = dataframe.valores.quantile(0.025)
    max_quantile = dataframe.valores.quantile(0.975)

    # Arredonda porque os valores são inteiros e fica melhor arredondando
    return round(min_quantile), round(max_quantile)