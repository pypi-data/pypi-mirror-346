# import numpy as np
import cv2 as cv


"""Array shape manipulations resizing"""
def scale_up(img, f=2):
    Y, X = img.shape
    return cv.resize(img, (X*f, Y*f))

def scale_down(img, f=2):
    Y, X = img.shape
    return cv.resize(img, (X//f, Y//f))

