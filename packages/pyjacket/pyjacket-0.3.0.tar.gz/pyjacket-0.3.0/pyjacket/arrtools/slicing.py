import numpy as np
import warnings

""" Slicing """
def _get_slice_locators(shape, area_fraction):
    f = np.sqrt(area_fraction/100)
    y, x = shape
    dx, dy = int(x*f), int(y*f)
    x0, y0 = (x - dx)//2, (y - dy)//2  # offset for centering
    return dx, dy, x0, y0

def slice_center(src, area_fraction=.25):
    dx, dy, x0, y0 = _get_slice_locators(src.shape, area_fraction)
    return src[y0: y0+dy, x0: x0+dx]

def slice_left(src, area_fraction=.25):
    dx, dy, _, y0 = _get_slice_locators(src.shape, area_fraction)
    return src[y0: y0+dy, :dx]
    
def slice_right(src, area_fraction=.25): 
    dx, dy, x0, y0 = _get_slice_locators(src.shape, area_fraction)
    return src[y0: y0+dy, -dx:]

def slice_top(src, area_fraction=.25): 
    dx, dy, x0, y0 = _get_slice_locators(src.shape, area_fraction)
    return src[:dy, x0: x0+dx]

def slice_bottom(src, area_fraction=.25): 
    dx, dy, x0, y0 = _get_slice_locators(src.shape, area_fraction)
    return src[-dy:, x0: x0+dx]

def slice_tl(src, area_fraction=.25): 
    dx, dy, x0, y0 = _get_slice_locators(src.shape, area_fraction)
    return src[:dy, :dx]
    
def slice_tr(src, area_fraction=.25): 
    dx, dy, x0, y0 = _get_slice_locators(src.shape, area_fraction)
    return src[:dy, -dx:]
    
def slice_bl(src, area_fraction=.25): 
    dx, dy, x0, y0 = _get_slice_locators(src.shape, area_fraction)
    return src[-dy:, :dx]
    
def slice_br(src, area_fraction=.25): 
    dx, dy, x0, y0 = _get_slice_locators(src.shape, area_fraction)
    return src[-dy:, -dx:]

def slice_around(arr, yx: tuple, shape=(5, 5), *, pad=None):
    """shape of odd integers
    TODO: allow pad to place a filler value instead of neglecting out of bounds
    """
    Y, X = arr.shape
    y0, x0 = yx
    y0 = int(round(y0))
    x0 = int(round(x0))
    dy, dx = shape[0]//2, shape[1]//2
    ymin, xmin = max(y0 - dy, 0), max(x0 - dx, 0)
    ymax, xmax = min(y0 + dy + 1, Y), min(x0 + dx + 1, X)
    return arr[ymin:ymax, xmin:xmax]



def unzip_channels(img: np.ndarray, channels=2):
    remainder = img.shape[0] % channels
    if remainder:
        warnings.warn(Warning('Encountered odd number of frames, omitting last frame(s)'))
        img = img[:-remainder]
    return img.reshape((img.shape[0]//channels, channels, *img.shape[1:]))

