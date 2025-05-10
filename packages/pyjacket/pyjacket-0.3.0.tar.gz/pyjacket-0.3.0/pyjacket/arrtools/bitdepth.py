import numpy as np

""" 
TODO: consider movies instead of images
"""

""" _____ Get array bit information _____"""
def type_max(dtype: np.dtype):
    """Get the maximum value that can be represented by the given data type"""
    try:                return np.finfo(dtype).max
    except ValueError:  return np.iinfo(dtype).max

def bytes(dtype: np.dtype):
    return dtype.itemsize

def bits(dtype):
    return 8 * bytes(dtype)

def saturated(img: np.ndarray):
    """Determine which pixels are saturated"""
    return img >= type_max(img.dtype)


""" _____ Type conversions _____"""
def round_astype(arr: np.ndarray, dtype=np.uint8):
    """Convert datatype without changing content. 
    
    Values may fall of dynamic range:
     100 (int8)  => 100 (uint8)
      -1 (int8)  =>   0 (uint8)
    -155 (int8)  =>   0 (uint8)
    
    255 (uint8)  => 127 (int8)
    """
    return np.rint(arr).astype(dtype)

def convert_type(arr: np.ndarray, dtype=np.uint8):
    """Convert datatype and applies a scale factor to contents.

    Resolution may be lost when scaling down to a lower bit-size.
    """
    src_max = type_max(arr.dtype) + 1
    dst_max = type_max(dtype) + 1
    
    if src_max > dst_max:
        scale_factor = src_max//dst_max
        scaled = arr // scale_factor
        return scaled.astype(dtype)

    if dst_max > src_max:
        scale_factor = dst_max//src_max
        return(arr.astype(dtype) + 1)*scale_factor - 1
        
    return
astype = convert_type  # alias

def distribute_astype(arr: np.ndarray, type: np.dtype):
    """Convert datatype and rescale content to use full dynamic range
    
    This minimizes loss in resolution, but brightness info is lost.
    """
    target_type_max = type_max(type)
    return rescale(arr, 0, target_type_max, dst_dtype=type) #.astype(type)

def saturate_astype(*args, **kwargs):
    """Convert datatype and rescale content to saturate part of the data
    
    Sacrifice dim and bright information to maintain good resolution for the bulk of data.
    """
    raise NotImplementedError()

""" _____ Rescaling functions _____ (change contents, but not dtype)"""
def rescale(arr: np.ndarray, lb, ub, dst_dtype=None, mi=None, ma=None) -> np.ndarray:
    """Fits the bits into the requested window.
    If the image is of type uint, convert it back after rescaling"""
    src_dtype = arr.dtype
    dst_dtype = dst_dtype or src_dtype
    # Convert to float32 for improved accuracy
    if src_dtype != np.float32 or dst_dtype != np.float32: 
        arr = arr.astype(np.float32) 
        arr = rescale(arr, lb, ub, np.float32)
        arr = round_astype(arr, dst_dtype or src_dtype)
        return arr
    
    # Rescale float dtypes    
    mi = mi if mi is not None else np.min(arr)
    ma = ma if ma is not None else np.max(arr)
    return (arr-mi) * (ub-lb)/(ma-mi) + lb

def normalize(arr: np.ndarray) -> np.ndarray[np.float32]:
    """Rescales contents between 0 and 1."""
    arr = arr.astype(np.float32)
    return rescale(arr, 0, 1, dst_dtype=np.float32)

def rescale_distribute(arr: np.ndarray): 
    """Rescale image to use the full bit range that the source image allows. """
    return rescale(arr, 0, type_max(arr.dtype))

def rescale_saturate(arr: np.ndarray, percent_bottom: float, percent_top: float):
    """rescale such as to saturate <p_lower>% of the pixels."""    
    i1 = np.percentile(arr, percent_bottom)
    i2 = np.percentile(arr, 100-percent_top)
    arr = fix_between(arr, 
                      round_astype(i1, arr.dtype),
                      round_astype(i2, arr.dtype))
    return rescale_distribute(arr)



"""_____ Truncations _____"""
def fix_between(arr, lb, ub):
    """Trucate data smaller than lb or greater than ub"""
    return truncate_above(truncate_below(arr, lb), ub)

def truncate_below(arr, lb):
    return np.where(arr < lb, lb, arr)
    
def truncate_above(arr, ub):
    return np.where(arr > ub, ub, arr)