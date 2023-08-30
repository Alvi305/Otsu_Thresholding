import os
import pydicom
import numpy as np
import scipy
import skimage.filters
import mahotas as mh
import matplotlib.pyplot as plt


def new_mask(image, threshold):
    normalize = image / np.iinfo(image.dtype).max
    gaussian_blur = skimage.filters.gaussian(normalize, sigma=1.0)
    binary = (gaussian_blur > threshold).astype('uint16')
    perimeter = mh.labeled.bwperim(binary)
    fill = scipy.ndimage.binary_fill_holes(perimeter).astype('uint16')
    return fill


if __name__ == '__main__':
    file = os.path.join(os.getcwd(), 'test.dcm')
    img = pydicom.dcmread(file)
    img = img.pixel_array
    mask_img, threshold = new_mask(img, 0.002)
    plt.imshow(mask_img)
    plt.show()