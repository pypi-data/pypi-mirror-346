import math
import numpy as np
import cv2

from typing import Union

from pyjacket import arrtools
from .models import ImageHandle, Metadata, ImageReader, ExifTag
# from pyjacket.filetools.image._image import ImageHandle


class MP4Reader(ImageReader):

    def read(self, file_path: str, **kwargs) -> np.ndarray:
        raise NotImplementedError()

    def read_lazy(self, file_path: str, **kwargs):
        raise NotImplementedError()

    def seq_read(self, file_path: str, **kwargs) -> np.ndarray:
        raise NotImplementedError()

    def seq_read_lazy(self, file_path: str, **kwargs):
        raise NotImplementedError()


    def read_meta(self, file_path: str, **kwargs):
        raise NotImplementedError()


    def write(self, file_path: str, data: np.ndarray, meta:Metadata=None, **kwargs):
        return write(file_path, data, meta, **kwargs)
        # raise NotImplementedError()

    def write_lazy(self, file_path: str, data: ImageHandle, meta:Metadata=None, **kwargs):
        raise NotImplementedError()



def read(filepath):
    ...

def write(filepath, data: np.ndarray, meta=None, frame_time=1/10, max_fps=60, scale=None):
    """Data needs to be 3d array of shape (frames, height, width)"""
    if data.ndim not in [3, 4]:
        raise ValueError(f"Cannot interpret data that has {data.ndim} dimensions")
    
    elif data.ndim == 3:
        raise NotImplementedError('Still need to do this sorry')
        # 3 dimensions: assume (t, h, w) => greyscale colormap

    # 4 dimensions: assume (t, h, w, ch)
    _, height, width, ch = data.shape
    is_color = bool(ch != 1)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4 is always lossy
    fps = 1 / frame_time
    if fps > max_fps:
        print('WARNING: Converting FPS')
        step = math.ceil(fps / max_fps)
        fps /= step
        data = data[::step]
    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height), isColor=is_color)

    # Define a percentage of pixels to saturate
    if scale is not None:
        lb, ub = scale.T
    else:
        lb, ub = 0, arrtools.type_max(data[0].dtype)

    for frame in data:
        # Brightness Scaling
        frame = frame.astype(np.float32)
        frame = arrtools.subtract_uint(frame, lb) * 255 // (ub - lb)
        frame[frame > 255] = 255
        frame = frame.astype(np.uint8)

        # False Color
        frame = false_color(frame, colors=[
            [255,   0, 255],
            [  0, 255,   0],
        ])
        out.write(frame) 
    out.release()  

def false_color(img: np.ndarray, colors: list[tuple]):
    """Convert multi-channel image data into a false-colored RGB image/movie""" 
    shape_out = (*img.shape[:-1], 3)
    
    Rmax, Gmax, Bmax = np.array(colors).sum(axis=0)

    
    out = np.zeros(shape_out, dtype=img.dtype)
    for i, (R, G, B) in enumerate(colors):
        channel = img[..., i]
        out[..., 0] += (channel.astype(np.uint32) * R // Rmax).astype(channel.dtype)
        out[..., 1] += (channel.astype(np.uint32) * G // Gmax).astype(channel.dtype)
        out[..., 2] += (channel.astype(np.uint32) * B // Bmax).astype(channel.dtype)
    return out

# def rearrange_dimensions(data, order):
#     for arr in data:
#         yield np.transpose(arr, order)


# def false_color_lazy(data, colors):
#     # convert channels
#     for arr in data:
#         yield false_color(arr, colors)

# def do_both(data, order, colors):
#     for arr in data:
#         arr = false_color(arr, colors)
#         arr = np.transpose(arr, order)
#         yield arr


    

        
        



# def write_grayscale(filepath, data: np.ndarray, meta=None, frame_time=1/10, max_fps=60):
#     """Data needs to be 3d array of shape (frames, height, width)"""
#     # Determine fps, ensuring it below max_fps
#     fps = 1 / frame_time
#     if fps > max_fps:
#         step = math.ceil(fps / max_fps)
#         fps /= step
#         data = data[::step]
        
#     # scale data to use full dynamic range
#     mi = np.min(data)
#     ma = np.max(data)
#     factor = 255/(ma - mi)

#     _, height, width = data.shape
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4 is always lossy
#     out = cv2.VideoWriter(filepath, fourcc, fps, (width, height), isColor=False)
#     for frame in data:

#         # This should be featured in arrtools ....
#         frame = frame.astype(np.float32)
#         frame = (frame - mi) * factor
#         frame = frame.astype(np.uint8)
        
#         out.write(frame) 
#     out.release()


# def write_color(filepath, data, meta=None, frame_time=1/10, max_fps=60, scale=None):
#     """openCV requires uint8 data, we convert it here, so uint16 input is OK"""

#     fps = 1 / frame_time
#     if fps > max_fps:
#         print('WARNING: Converting FPS')
#         step = math.ceil(fps / max_fps)
#         fps /= step
#         data = data[::step]
        
        
#     # Define a percentage of pixels to saturate
#     if scale is not None:
#         lb, ub = scale
#     else:
#         lb, ub = 0, arrtools.type_max(data[0].dtype)

#     _, height, width, colors = data.shape
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4 is always lossy
#     out = cv2.VideoWriter(filepath, fourcc, fps, (width, height), isColor=True)
    
#     # print(f"\nRescaling data...")
#     for frame in data:
#         # print(frame[0, :10], frame.shape)

#         # Rescale data between lb and ub and cast to np.uint8
#         frame = frame.astype(np.float32)
#         frame = arrtools.subtract_uint(frame, lb) * 255 // (ub - lb)
#         frame[frame > 255] = 255
#         frame = frame.astype(np.uint8)
        
#         out.write(frame) 
#     out.release()


    
# def read_exif(filename):
    # ...