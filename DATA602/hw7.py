import timeit

setup = '''
import pandas as pd
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit

# file imported from local directory
df = pd.read_csv('C:/Users/bhao/Google Drive/CUNY/git/DATA602/brainandbody.csv')
# df = pd.read_csv('~/Google Drive/CUNY/git/DATA602/brainandbody.csv')

def formulaic_approach():
    # using formulaic approach
    x_bar = np.mean(df['brain'])
    y_bar = np.mean(df['body'])
    slope = sum((df['brain'] - x_bar) * (df['body'] - y_bar)) / sum((df['brain'] - x_bar)**2)
    intercept = y_bar - slope * x_bar
    print('Formulaic approach: y = %f + %f * x') % (intercept, slope)


def linalg_approach():
    # using linear algebra approach
    A = pd.DataFrame({'a1': 1,
                       'a2': df['brain']})
    b = df['body']
    AtA = np.matmul(A.T, A)
    x_hat = np.matmul(np.linalg.pinv(AtA),
                      np.matmul(A.T, b))
    print('Linear algebra approach: y = %f + %f * x') % (x_hat[0], x_hat[1])


def scipy_stats_approach():
    # using scipy linear model approach
    x = df['brain']
    y = df['body']
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    print('Scipy stats approach: y = %f + %f * x') % (intercept, slope)


def scipy_curve_fit_approach():
    # using scipy curve_fit approach
    def func(x, a, b):
        return a * x + b

    x = df['brain']
    y = df['body']
    popt, pcov = curve_fit(func, x, y)
    print('Scipy curve_fit approach: y = %f + %f * x') % (popt[1], popt[0])
'''

if __name__ == '__main__':
    n = 1
    t = timeit.Timer('formulaic_approach()', setup=setup)
    print 'Sort using formulaic_approach()           : %f' % (t.timeit(n))
    t = timeit.Timer('linalg_approach()', setup=setup)
    print 'Sort using linalg_approach())             : %f' % (t.timeit(n))
    t = timeit.Timer('scipy_stats_approach()', setup=setup)
    print 'Sort using scipy_stats_approach()         : %f' % (t.timeit(n))
    t = timeit.Timer('scipy_curve_fit_approach()', setup=setup)
    print 'Sort using scipy_curve_fit_approach()     : %f' % (t.timeit(n))

