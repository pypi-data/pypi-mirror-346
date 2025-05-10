

"""Build colors using sliders"""
from typing import List
import cv2
import numpy as np


import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

print(dir_path)


def color_picker_rgb() -> List[int]:
    return



def color_picker_hsv():


    frame = cv2.imread(f'{dir_path}\\colormap.jfif')
    print(frame.shape)
    
    
    frame = cv2.resize(frame, (512, 512))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # # Create trackbars for color selection
    cv2.namedWindow('image')
    
    # cv2.imshow('image', frame)
    cv2.createTrackbar('HMin', 'image', 0, 179, lambda x: None)
    

    cv2.createTrackbar('SMin', 'image', 0, 255, lambda x: None)
    cv2.createTrackbar('VMin', 'image', 0, 255, lambda x: None)

    cv2.createTrackbar('HMax', 'image', 0, 179, lambda x: None)
    cv2.createTrackbar('SMax', 'image', 0, 255, lambda x: None)
    cv2.createTrackbar('VMax', 'image', 0, 255, lambda x: None)
    cv2.setTrackbarPos('HMax', 'image', 179)
    cv2.setTrackbarPos('SMax', 'image', 255)
    cv2.setTrackbarPos('VMax', 'image', 255)

    while not (cv2.waitKey(1) & 0xFF == ord('q')):
        # Set the lower and upper ranges of the HSV image
        lower_range = np.array([
            cv2.getTrackbarPos('HMin', 'image'), 
            cv2.getTrackbarPos('SMin', 'image'), 
            cv2.getTrackbarPos('VMin', 'image')
            ])

        upper_range = np.array([
            cv2.getTrackbarPos('HMax', 'image'), 
            cv2.getTrackbarPos('SMax', 'image'), 
            cv2.getTrackbarPos('VMax', 'image')
            ])

        # Create and apply mask
        mask = cv2.inRange(hsv, lower_range, upper_range)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        # Show the resulting images
        cv2.imshow('image', res)

    # Release the camera and close all windows

    cv2.waitKey(0)
    cv2.destroyAllWindows()




if __name__ == '__main__':
    color_picker_hsv()