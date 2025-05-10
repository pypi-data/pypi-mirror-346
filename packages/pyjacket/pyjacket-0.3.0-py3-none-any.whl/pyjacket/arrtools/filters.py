import cv2 as cv
import numpy as np

from pyjacket import arrtools

def subtract_uint(a, b):
    return np.where(a > b, a-b, 0)

def subtract_percentile(image, p: float=50.):
    intensity_threshold = np.percentile(image, p)
    return np.where(image > intensity_threshold, image-intensity_threshold, 0)


""" Convolutional Percentile Filters """
def percentile_filter(*args, **kwargs):
    raise NotImplementedError

def min_filter(image, size, *args, **kwargs):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, size)
    return cv.erode(image, kernel, *args, **kwargs)

def max_filter(image, size, *args, **kwargs):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, size)
    return cv.dilate(image, kernel, *args, **kwargs)

def median_filter(image, size, subtract=False, **kwargs):
    background = cv.medianBlur(image, size, **kwargs)
    if subtract:
        return subtract_uint(image, background)
    else:
        return background
    
def subtract_median(a, size, *args, **kwargs):
    a = arrtools.distribute_astype(a, np.uint8)
    b = median_filter(a, size, *args, **kwargs)
    return subtract_uint(a, b)
    

""" Linear convolutional filters """
def boxcar(m, shape, ddepth=-1):
    return cv.boxFilter(m, ddepth, shape)

def gaussian_blur(src, ksize: tuple, sigmaX=0, **kwargs):
    return cv.GaussianBlur(src, ksize, sigmaX, **kwargs)

"""FFT Filters"""
def band_pass(src, r1=None, r2=None, c1=None, c2=None):
    X = np.fft.fft2(src)
    Xf = np.zeros(X.shape, dtype=np.complex128)
    Xf[r1:r2, c1:c2] = X[r1:r2, c1:c2]
    dst = np.fft.ifft2(Xf)
    return np.abs(dst)




def band_pass(src, low, high):
    f = np.fft.fft2(src)

    # Shift zero-frequency component to the center of the spectrum
    fshift = np.fft.fftshift(f)

    shape = src.shape
    x = np.arange(-shape[1] // 2, shape[1] // 2)
    y = np.arange(-shape[0] // 2, shape[0] // 2)
    xx, yy = np.meshgrid(x, y)
    mask = (low <= np.sqrt(xx**2 + yy**2)) & (np.sqrt(xx**2 + yy**2) <= high)
    mask = mask.astype(float)

    # # Create bandpass filter
    # mask = bandpass(image.shape, low, high)

    # Apply filter to shifted spectrum
    fshift_filtered = fshift * mask

    # Shift filtered spectrum back
    f_filtered = np.fft.ifftshift(fshift_filtered)

    # Perform inverse 2D FFT
    image_filtered = np.real(np.fft.ifft2(f_filtered))
    return image_filtered














def high_pass(x, f1, f2=None):
    f2 = f2 or f1
    R, C = x.shape
    a, b = int(f1*R), int(f2*C)
    return band_pass(x, a, None, b, None)

def low_pass(x, f1, f2=None):
    f2 = f2 or f1
    R, C = x.shape
    a, b = int(f1*R), int(f2*C)
    return band_pass(x, None, a, None, b)



"""Other filters"""
def denoise(src: np.ndarray[np.uint8], h=15) -> np.ndarray[np.uint8]:
    return cv.fastNlMeansDenoising(src, h=h)  # -> uint8
