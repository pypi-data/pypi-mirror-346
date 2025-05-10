import numpy as np

"""Tools for arrays representing histograms

[1, 3, 5, 4, 4, 1, 0, 0, 0, 3] =>

|      #
|      #  #  #
|   #  #  #  #              #
|   #  #  #  #              #
|#__#__#__#__#__#__ __ __ __#
.0  1  2  3  4  5  6  7  8  9 
"""

# def hist_median(arr: np.ndarray, n=None):
#     n = n if n is not None else arr.sum()
#     running_sum = 0
#     for median, freq in enumerate(arr):
#         running_sum += 2*freq
#         if running_sum >= (n+1):
#             break
#     return median

def hist_median(arr: np.ndarray, n):
    """n: total frequency, which will be odd for an odd kernel-size"""
    return np.searchsorted(arr.cumsum(), (n+1)//2)