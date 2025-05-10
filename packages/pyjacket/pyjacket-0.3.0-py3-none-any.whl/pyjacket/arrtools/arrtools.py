from typing import Optional, Union
import numpy as np
import cv2 as cv

"""Debugging"""
# def intel(movie):
#     """Print a summary of imarray properties"""
#     size, unit = format_bytes(movie.size * movie.itemsize)
#     print("\n".join((
#         f"movie shape: {movie.shape},  [dtype: {movie.dtype}]",
#         f"intensity range: {movie.min()} - {movie.max()}",
#         f"memory: {size} {unit}",
#     )))


"""Access bit depth information"""
def type_max(dtype):
    """Get the maximum value that can be represented by the given data type"""
    try:                return np.finfo(dtype).max
    except ValueError:  return np.iinfo(dtype).max

def bits(x: Union[np.ndarray, np.dtype]):
    """Number of bits (1s & 0s) used to encode a number of the given data type"""
    if isinstance(x, np.ndarray):
        return 8 * x.dtype.itemsize
    elif isinstance(x, np.dtype):
        return 8 * x.itemsize
    else:
        raise ValueError(f'x must be an array or a dtype object. got {type(x) = }')


""" Bit depth manipulations"""
def format_bytes(size):
    """1024 Bytes -> 1 KB"""
    power = 2**10
    n = 0
    power_labels = {0 : 'Bytes', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:  # I think this can be replaced by a log for speedup
        size /= power
        n += 1
    return size, power_labels[n]

def normalize_image(image, mi=None, ma=None):
    image = image.astype(np.float32)
    mi = mi or image.min()
    ma = ma or image.max()
    return (image - mi) / (ma - mi) if mi != ma else image*0

def convert_and_rescale(m, dst_type: np.dtype=np.uint8): # [x tested]
    """Convert type and rescale data if bit depth changes """
    # determine which data type can capture larger numbers, to optimize precision
    src_max = type_max(m.dtype)
    dst_max = type_max(dst_type)
    m = m.astype(dst_type) if dst_max > src_max else m

    # in case of floats
    if src_max > 1e20:  src_max = 0  
    if dst_max > 1e20:  dst_max = 0

    if dst_max > src_max:
        f = (dst_max + 1) // (src_max + 1)
        m = m * f
    else:
        f = (src_max + 1) // (dst_max + 1)
        m = m / f 
    return m.astype(dst_type)


"""Array shape manipulations resizing"""
def scale_up(img, f=2):
    Y, X = img.shape
    return cv.resize(img, (X*f, Y*f))

def scale_down(img, f=2):
    Y, X = img.shape
    return cv.resize(img, (X//f, Y//f))


"""Image moments: (get these from opencv)"""
def centroid(w, offset=(0, 0)):
    y0, x0 = offset
    wt = w.sum()
    
    if w.ndim == 1:
        ny, = w.shape
        xc = 0
        yc = (w @ np.arange(ny)) / wt
    
    elif w.ndim == 2:
        ny, nx = w.shape
        xc = (w.sum(axis=0) @ np.arange(nx)) / wt
        yc = (w.sum(axis=1) @ np.arange(ny)) / wt
    
    else:
        raise NotImplementedError("Cannot determine centroid in 3 or more dimensions")
    
    return np.array([yc+y0, xc+x0])
        
def _centroid1d(w, offset):
    y0, x0 = offset
    nx, = w.shape
    return np.array([(w @ np.arange(nx)) / w.sum() + y0, x0])
      
def _centroid2d(W, offset=(0, 0)):
    y0, x0 = offset
    ny, nx = W.shape
    Wt = W.sum()
    x_c = (W.sum(axis=0) @ np.arange(nx)) / Wt
    y_c = (W.sum(axis=1) @ np.arange(ny)) / Wt
    return np.array([y_c + y0, x_c + x0])


""" Element-wise Filters """
def ensure_below(src, ub=1):
    """Equivalent to min(src, lb)"""
    return np.where(src > ub, ub, src)

def ensure_above(src, lb=0):
    """Equivalent to max(src, lb)"""
    return np.where(src < lb, lb, src)

def ensure_between(src, lb=0, ub=1):
    """Equivalent to min(max(a, src), b)"""
    return ensure_below(ensure_above(src, lb), ub)


""" Convolutional filters (local filters)"""
def boxcar(m, shape, ddepth=-1):
    return cv.boxFilter(m, ddepth, shape)

# def boxcar(m, shape, ddepth=-1): return cv.filter2D(m, ddepth, np.ones(shape)/np.prod(shape))

def gaussian_blur(image, shape=(1, 1), sigmaX=cv.BORDER_DEFAULT, *args):
    image = cv.GaussianBlur(image, shape, sigmaX, *args)  
    return normalize_image(image)

def median_filter(src: np.ndarray[np.float32], *args, **kwargs) -> np.ndarray[np.float32]:
    background = cv.medianBlur(convert_and_rescale(src, np.uint8), *args, **kwargs) / 255 # -> uint8
    subtracted = src - background.astype(np.float32)
    subtracted = ensure_between(subtracted)  # this should be an optional param
    subtracted = normalize_image(subtracted)
    return subtracted, background


"""FFT Filters"""
def band_pass(src, r1=None, r2=None, c1=None, c2=None):
    X = np.fft.fft2(src)
    Xf = np.zeros(X.shape, dtype=np.complex128)
    Xf[r1:r2, c1:c2] = X[r1:r2, c1:c2]
    dst = np.fft.ifft2(Xf)
    return normalize_image(np.abs(dst))

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
def denoise(src: np.ndarray[np.float32], h=15):
    filtered = cv.fastNlMeansDenoising(convert_and_rescale(src, np.uint8), h=h)  # -> uint8
    filtered = normalize_image(filtered)  # -> float32
    return filtered


"""Contour methods (move this to another library"""
def select_inside(grey, contour, bbox=None):  # can remove grey
    """go through a bounding box and select everything inside the contour"""
    x0, y0, dx, dy = bbox or cv.boundingRect(contour)
    arr = np.zeros(grey.shape, dtype=bool)
    for y in range(y0, y0 + dy):
        for x in range(x0, x0 + dx):
            arr[y, x] = (cv.pointPolygonTest(contour, (x, y), measureDist=False) >= 0)
    return arr
