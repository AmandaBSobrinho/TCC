from numpy.random import seed
from scipy.stats import anderson


def normality(data):
    seed(1)
    result = anderson(data)
    normal = []

    for i in range(len(result.critical_values)):
        sl, cv = result.significance_level[i], result.critical_values[i]
        if result.statistic < result.critical_values[i]:
            normal.append(1)
            # print('%.3f: %.3f, dados parecem normais (falha em rejeitar H0)' % (sl, cv))
        else:
            normal.append(0)
            # print('%.3f: %.3f, dados nao parecem normais (rejeitam H0)' % (sl, cv))

    if normal.count(1) >= 3:
        return 1
    else:
        return 0
