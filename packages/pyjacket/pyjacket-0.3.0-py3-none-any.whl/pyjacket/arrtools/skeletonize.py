
import cv2 as cv
from numpy import uint8
import numpy as np


def skeletonize(img, intensity_threshold=10):
    _, img = cv.threshold(img, intensity_threshold, 255, type=cv.THRESH_BINARY)
    return cv.ximgproc.thinning(img)

def get_skeleton_coordinates(skel):
    contours, _ = cv.findContours(skel, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    chains = []
    for i in range(len(contours)):
        m = np.zeros_like(skel)
        cv.drawContours(m, contours, i,  color=255, thickness=-1)
        yx = np.array(np.where(m == 255))
        chains.append(yx)
    return chains

# def draw_skeleton():
#     # overlay skeletons with raw image
#     # dont use coordinates
#     # instead use the skeletonized image as a mask
#     pass


if __name__ == '__main__':
    from src.pyx.arrtools import scale_down as scale
    
    scale_f = 2

    # Raw image
    # loc = r"C:\Users\arfma005\GitHub\ffspec\data\1900-01-01\test001\preprocessed_feature003.tif"
    loc = r"C:\Users\arfma005\GitHub\ffspec\results\1900-01-01\test001\preprocess\002_preprocessed.tif"
    img = cv.imread(loc, cv.IMREAD_GRAYSCALE)
    cv.imshow('raw image', scale(img, scale_f))

    skel = skeletonize(img, 80)
    cv.imshow('skeleton', scale(skel, scale_f))
    cv.waitKey(0)

    backbones = get_skeleton_coordinates(skel)
    print(backbones)
    print(len(backbones))