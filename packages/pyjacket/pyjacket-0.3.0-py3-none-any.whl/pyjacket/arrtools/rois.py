# import pandas as pd


import cv2
# from trash.line_profile import get_line_profile
# from .pyx.arrtools import boxcar, centroid, convert_and_rescale, intel, slice_around, ensure_above
# from .filer import read_image_sequence
# import matplotlib.pyplot as plt
# from numpy import uint8
import numpy as np

# from pyjacket.filetools import ImageHandle
from . import slicing, arrtools, filters

class ROI:
    
    def __init__(self, x0, y0, dx, dy):
        self.x0 = x0
        self.y0 = y0
        self.dx = dx
        self.dy = dy
        
    def top_left(self): ...
    
    def top_right(self): ...
    
    def bottom_left(self): ...
    
    def bottom_right(self): ...
    
    @property
    def x1(self):
        return self.x0 + self.dx
    
    @property
    def y1(self):
        return self.y0 + self.dy
        
    def apply(self, img: np.ndarray):
        x0 = self.x0
        y0 = self.y0
        
        # x1 = x0 + dx
        # y1 = y0 + dy
        
        x1 = self.x1
        y1 = self.y1

        if img.ndim == 2:
            cropped = img[y0:y1, x0:x1]
            
        elif img.ndim == 3:
            cropped = img[:, y0:y1, x0:x1]
            
        elif img.ndim == 4:
            cropped = img[:, y0:y1, x0:x1, :]
            
        return cropped
    
    def __repr__(self):
        return f'ROI({self.x0}, {self.y0}, {self.dx}, {self.dy})'



def select_ROI(img: np.ndarray, rescale=True):
    """ndarrray, or ImageHandle"""
    
    # if isinstance(img, ImageHandle):
    #     img = img.thumbnail
    
    
    
    if img.ndim == 2:    preview = img
    elif img.ndim == 3:  preview = img[0]
    
    if rescale:
        preview = arrtools.rescale_distribute(preview)
        
    winname = 'Please select a region of interest' 
    roi = cv2.selectROI(winname, preview)
    cv2.destroyWindow(winname)
    return ROI(*roi)
        




# def refine_roi(imgp, center, roi_shape):
#     """Recenter a feature using center of mass"""
#     speed = 3
#     max_cycles = 10
    
#     center_y, center_x = center
    
#     half_roi_shape = np.array(roi_shape) / 2
#     for i in range(max_cycles):

#         img_slice = slicing.slice_around(imgp, (center_y, center_x), roi_shape)
#         com = arrtools.centroid(img_slice)
#         dy, dx = half_roi_shape - com
#         # print(f"{dy, dx = }, {com = }")
#         center_y -= speed * dy
#         center_x -= speed * dx

#         # img_slice = ar.slice_around(imgp, (center_y, center_x), roi_shape)
#         # img_slice = ar.normalize_uint8(img_slice)
#         # cv.imshow(f'feature offset {i}', cv.resize(img_slice, (800, 100)))
        
#         # alternatively: if offset was seen before
#         if max(abs(dy), abs(dx)) < 1:
#             break
        
#     return center_y, center_x




# def get_ROI(df, frame, feature, roi_shape=(50, 100)):
#     df = df.loc[df['frame'] == frame]
#     x = int(round(df['x'][feature]))
#     y = int(round(df['y'][feature]))
#     dy, dx = roi_shape
#     ymin, ymax, xmin, xmax = y-dy-2, y+dy, x-dx, x+dx
#     return ymin, ymax, xmin, xmax

# def find_center_in_vslice(roi, col: int, slice_shape: tuple):
#     y, x = roi.shape
#     yc, xc = y//2, x//2
#     # print('y center in ROI:', yc)
#     dy, dx = slice_shape
    
#     # make sure the DNA is roughly centered in the ROI
#     for _ in range(10):
#         # print(yc, xc)
#         subroi = slicing.slice_around(roi, (yc, col), (dy, dx))
#         yc_sub, _ = arrtools.centroid(subroi)
#         nudge = yc_sub - (dy//2)
#         # yc += int(round(nudge))
        
#         if abs(nudge) < 1:
#             yc += nudge
#             return yc

#         yc += int(round(nudge))
            
        
#         # print('y center in subroi:', yc_sub)
        
#         # print('y center in ROI:', yc)
#         dy = int(dy*1)
        
#     raise Warning('finding the center of the DNA did not converge')

# def horizontal_line_profile(roi, p, slice_shape=(15, 15), vincinity=(5, 5)):
#     """N.B. ensure the roi is preprocessed!"""
#     centers = []
#     roi_boxcar = filters.boxcar(roi, vincinity)
#     thresh = np.percentile(roi_boxcar, p)
#     for xc in range(1, roi.shape[1]-slice_shape[1]-1):    # no magic numbers
#         yc = find_center_in_vslice(roi, xc, slice_shape)
#         yc_int = int(round(yc))
#         env = slicing.slice_around(roi, (yc_int, xc), vincinity)
#         local_intensity = env.mean()
#         if local_intensity > thresh:
#             centers.append([xc, yc])
        
#     x, y = np.array(centers).T
#     return x, y

# def denoise_percentile_treshold(img, p):
#     cutoff = np.percentile(img, p)
#     img = ensure_above(img, cutoff) - cutoff
#     return img

# def main():
#     frame_nr = 0
#     roi_nr = 3

#     # Read the image
#     # raw_img = read_image_sequence(r"data\1900-01-01\test001\test_movie002.tif")[frame_nr]
#     # img = convert_and_rescale(raw_img, uint8)  # -> uint8 image

#     # Denoise the image
#     img = denoise_percentile_treshold(img, 80)

#     # get a ROI
#     roi_shape = (20, 60)  # y, x
#     slice_shape = (5, 5)  # y, x
#     df = pd.read_csv(r"results\1900-01-01\test001\trajectories.csv", sep='\t', index_col=0)
#     ymin, ymax, xmin, xmax = get_ROI(df, frame_nr, roi_nr, roi_shape=roi_shape) 
#     roi = img[ymin: ymax, xmin: xmax]

#     # Obtain the horizontal line profile. N.B. enter a denoised roi!
#     x, y = horizontal_line_profile(roi, p=90, slice_shape=slice_shape, vincinity=(5, 5))
#     print(x, y)

#     plt.imshow(roi, cmap='gray')
#     plt.plot(x, y, 'r')
#     plt.show()


# if __name__ == "__main__":
#     main()