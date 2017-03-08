import pandas as pd
import numpy as np
from scipy import stats

# file imported from local directory
df = pd.read_csv('C:/Users/bhao/Google Drive/CUNY/git/DATA602/brainandbody.csv')

# using formulaic approach
x_bar = np.mean(df['brain'])
y_bar = np.mean(df['body'])
slope = sum((df['brain'] - x_bar) * (df['body'] - y_bar)) / sum((df['brain'] - x_bar)**2)
intercept = y_bar - slope * x_bar
print('Formulaic approach: y = %f + %f * x') % (intercept, slope)


# using linear algebra approach
A = pd.DataFrame({'a1': 1,
                   'a2': df['brain']})
b = df['body']
AtA = np.matmul(A.T, A)
x_hat = np.matmul(np.linalg.pinv(AtA),
                  np.matmul(A.T, b))
print('Linear algebra approach: y = %f + %f * x') % (x_hat[0], x_hat[1])


# using scipy linear model approach
x = df['brain']
y = df['body']
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
print('Scipy stats approach: y = %f + %f * x') % (intercept, slope)
