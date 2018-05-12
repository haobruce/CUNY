import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.misc import imread
import scipy.ndimage as ndimage
import mahotas as mh


# 1) plot cars data
cars = pd.read_csv('/Users/brucehao/Google Drive/CUNY/git/DATA602/cars.data.csv', header=None)
cars.columns = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class']
cars.head()

fig = plt.figure()
for i, col in enumerate(['buying', 'maint', 'safety', 'doors']):
    ax = fig.add_subplot(2, 2, i + 1)
    temp = cars.groupby(col)[col].count()
    sns.barplot(temp.index, temp.values)
    ax.set_ylabel('frequency')
plt.tight_layout()
plt.show()


# 2) plot regression results
bab = pd.read_csv('/Users/brucehao/Google Drive/CUNY/git/DATA602/brainandbody.csv')

sns.regplot(bab['brain'], bab['body'], scatter=True)
plt.show()


# 3) plot object centers
# objects.png img
img = imread('/Users/brucehao/Google Drive/CUNY/git/DATA602/objects.png')
imgf = ndimage.gaussian_filter(img, 3)
thres = imgf > imgf.mean()

# count and label objects
labeled, nr_objects = mh.label(thres)

# find coordinates for centers of mass
com = mh.center_of_mass(thres, labeled)
plt.plot(com[:, 1], com[:, 0], 'r.')
plt.xlim([0, img.shape[1]])
plt.ylim([img.shape[0], 0])
plt.imshow(img)
plt.show()


# 4) plot HTTP data
epa = pd.read_csv('/Users/brucehao/Google Drive/CUNY/git/DATA602/epa-http.txt',
                    header=None, sep='\s+', error_bad_lines=False)

# assign column names
epa.columns = ['host', 'date', 'request', 'reply', 'bytes']

# busiest hour in terms of requests
# add hour column based on datetime split
epa['hour'] = epa['date'].str.split(":").str[1]
epa.head()
hour = epa.groupby('hour')['hour'].count()
sns.tsplot(hour.values, hour.index)
plt.ylabel('number of requests')
plt.show()
