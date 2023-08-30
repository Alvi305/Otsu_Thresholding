import os
import pydicom
import numpy as np
import scipy
import skimage.filters
import mahotas as mh
import matplotlib.pyplot as plt


def mask(image):
    normalize = image / np.iinfo(image.dtype).max
    gaussian_blur = skimage.filters.gaussian(normalize, sigma=1.0)
    threshold = (skimage.filters.threshold_otsu(gaussian_blur))
    binary = (gaussian_blur > threshold).astype('uint16')
    perimeter = mh.labeled.bwperim(binary)
    fill = scipy.ndimage.binary_fill_holes(perimeter).astype('uint16')
    return fill, threshold


if __name__ == '__main__':
    file = os.path.join(os.getcwd(), 'test.dcm')
    img = pydicom.dcmread(file)
    img = img.pixel_array
    mask_img, threshold = mask(img)
    plt.imshow(mask_img)
    plt.show()