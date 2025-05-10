""" A skeleton is a grid whose features are 1-pixel wide"""

import numpy as np
from scipy.ndimage import convolve
import numpy as np

BRANCH_PATTERNS = np.array([
    [[0, 1, 0],
     [1, 1, 1],
     [0, 0, 0]],

    [[1, 0, 1,],
     [0, 1, 0,],
     [1, 0, 0,]],

    [[1, 0, 1],
     [0, 1, 0],
     [0, 1, 0]],

    [[0, 1, 0],
     [1, 1, 0],
     [0, 0, 1]],

    [[0, 0, 1],
     [1, 1, 1],
     [0, 1, 0]],

    [[1, 0, 0],
     [1, 1, 1],
     [0, 1, 0]],

    [[0, 1, 0],
     [1, 1, 0],
     [0, 1, 0]],

    [[0, 0, 0],
     [1, 1, 1],
     [0, 1, 0]],

    [[0, 1, 0],
     [0, 1, 1],
     [0, 1, 0]],

    [[1, 0, 0],
     [0, 1, 0],
     [1, 0, 1]],

    [[0, 0, 1],
     [0, 1, 0],
     [1, 0, 1]],

    [[1, 0, 1],
     [0, 1, 0],
     [0, 0, 1]],

    [[1, 0, 0],
     [0, 1, 1],
     [1, 0, 0]],

    [[0, 1, 0],
     [0, 1, 0],
     [1, 0, 1]],

    [[0, 0, 1],
     [1, 1, 0],
     [0, 0, 1]],

    [[0, 0, 1],
     [1, 1, 0],
     [0, 1, 0]],

    [[1, 0, 0],
     [0, 1, 1],
     [0, 1, 0]],

    [[0, 1, 0],
     [0, 1, 1],
     [1, 0, 0]],

    [[1, 1, 0],
     [0, 1, 1],
     [0, 1, 0]],

    [[0, 1, 0],
     [1, 1, 1],
     [1, 0, 0]],

    [[0, 1, 0],
     [1, 1, 0],
     [0, 1, 1]],

    [[0, 1, 0],
     [0, 1, 1],
     [1, 1, 0]],

    [[0, 1, 0],
     [1, 1, 1],
     [0, 0, 1]],

    [[0, 1, 1],
     [1, 1, 0],
     [0, 1, 0]],

    [[0, 1, 0],
     [1, 1, 1],
     [0, 1, 0]],

    [[1, 0, 1],
     [0, 1, 0],
     [1, 0, 1]],
    
    ])

NEIGHBOR_KERNEL = np.array([[1, 1, 1], 
                            [1, 0, 1], 
                            [1, 1, 1]])

def critical_points(skeleton: np.ndarray):
    """Finds end points and branch points for a skeleton image"""
    assert skeleton.dtype == np.uint8, ValueError('Skeleton must be np.uint8')
    
    neighbor_count = convolve(skeleton, NEIGHBOR_KERNEL, mode="constant", cval=0)

    end_points = np.argwhere(skeleton & (neighbor_count == 1))

    branch_candidates = np.argwhere(skeleton & (neighbor_count >= 3))
    branch_points = [yx for yx in branch_candidates if is_branch_point(skeleton, *yx)]
    return end_points, branch_points

def is_branch_point(skeleton: np.ndarray, y, x):

    padded_region = np.zeros((3, 3), dtype=skeleton.dtype)


    # Get the valid region indices
    y_start, y_end = max(0, y-1), min(skeleton.shape[0], y+2)
    x_start, x_end = max(0, x-1), min(skeleton.shape[1], x+2)

    # Compute the corresponding indices in the 3x3 patch
    patch_y_start, patch_y_end = 1 - (y - y_start), 1 + (y_end - y)
    patch_x_start, patch_x_end = 1 - (x - x_start), 1 + (x_end - x)

    # Copy valid data from skeleton into the 3x3 region
    padded_region[patch_y_start:patch_y_end, patch_x_start:patch_x_end] = skeleton[y_start:y_end, x_start:x_end]


    return any((
        np.all(pattern==padded_region) \
            for pattern in BRANCH_PATTERNS
    ))
