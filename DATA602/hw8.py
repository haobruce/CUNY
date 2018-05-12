import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
from scipy.misc import imsave
import scipy.ndimage as ndimage
import mahotas as mh


# circles.png img
img = imread('C:\\Users\\bhao\\Google Drive\\CUNY\\git\\DATA602\\circles.png')
imgf = ndimage.gaussian_filter(img, 16)
thres = imgf > np.percentile(imgf, [90])  # 90th percentile needed to separate into 5 objects

# count and label objects
labeled, nr_objects = mh.label(thres)
plt.imshow(labeled)
plt.show()

# find coordinates for centers of mass
com = mh.center_of_mass(thres, labeled)
plt.plot(com[:, 1], com[:, 0], 'r.')
plt.xlim([0, img.shape[1]])
plt.ylim([img.shape[0], 0])
plt.imshow(thres)
plt.show()

print('Circles.png:')
print('Number of objects:    %d') % nr_objects
print('Coordinates of object centers:')
print(com)


# objects.png img
img = imread('C:\\Users\\bhao\\Google Drive\\CUNY\\git\\DATA602\\objects.png')
imgf = ndimage.gaussian_filter(img, 3)
thres = imgf > imgf.mean()
imsave('C:\\Users\\bhao\\Google Drive\\CUNY\\git\\DATA602\\objects2.png', thres)

# count and label objects
labeled, nr_objects = mh.label(thres)
#plt.imshow(labeled)    # not sure why I can't show this image; keep getting
#plt.show()             # ValueError: 3-dimensional arrays must be of dtype unsigned byte

# find coordinates for centers of mass
com = mh.center_of_mass(thres, labeled)
plt.plot(com[:, 1], com[:, 0], 'r.')
plt.xlim([0, img.shape[1]])
plt.ylim([img.shape[0], 0])
plt.imshow(img)
plt.show()

print('Circles.png:')
print('Number of objects:    %d') % nr_objects
print('Coordinates of object centers:')
print(com)


# CLEARLY IN THIS CASE, GAUSSIAN FILTERING DOES NOT WORK WELL
# It mainly picks up the lighter areas as objects
# Try using a filter that picks up object outlines instead
# peppers.png img
img = imread('C:\\Users\\bhao\\Google Drive\\CUNY\\git\\DATA602\\peppers.png')
imgf = ndimage.gaussian_filter(img, 8)
thres = imgf > imgf.mean()
imsave('C:\\Users\\bhao\\Google Drive\\CUNY\\git\\DATA602\\peppers2.png', thres)

# count and label objects
labeled, nr_objects = mh.label(thres)
#plt.imshow(labeled)    # not sure why I can't show this image; keep getting
#plt.show()             # ValueError: 3-dimensional arrays must be of dtype unsigned byte

# find coordinates for centers of mass
com = mh.center_of_mass(thres, labeled)
plt.plot(com[:, 1], com[:, 0], 'r.')
plt.xlim([0, img.shape[1]])
plt.ylim([img.shape[0], 0])
plt.imshow(img)
plt.show()

print('Circles.png:')
print('Number of objects:    %d') % nr_objects
print('Coordinates of object centers:')
print(com)
