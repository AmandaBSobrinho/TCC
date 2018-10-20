def calculate(dataframe):

    min_quantile = dataframe.valores.quantile(0.025)
    max_quantile = dataframe.valores.quantile(0.975)

    return round(min_quantile), round(max_quantile)