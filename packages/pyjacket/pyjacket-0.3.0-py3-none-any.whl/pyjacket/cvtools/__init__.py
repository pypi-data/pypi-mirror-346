print('imported cvtools')

# from .color_picker import color_picker_hsv

import numpy as np

# from ._imread.nd2 import imread_nd2, MetadataND2
# from ._imread.tif import imread_tif

from PIL import Image, ImageSequence


import matplotlib.pyplot as plt


def imread_tif(filepath, as_gray=False):
    # Read an RGB .tiff file
    movie = Image.open(filepath)
    result = []
    for frame in ImageSequence.Iterator(movie):
        
        if as_gray:
            frame = frame.convert('L')
            
        result.append(frame)
    movie = np.array(result)
    return movie
    

def imread_nd2(filepath):
    return f"{filepath}.nd2"



def imread(filepath: str, *args, **kwargs) -> np.ndarray:
    """
    """
    if not '.' in filepath: raise ValueError(f"missing extension in filename: {filepath}")
    
    ext = filepath.split('.')[-1]
    
    # allow reading various data formats
    read_function = {
        'nd2': imread_nd2,
        'tif': imread_tif,
    }.get(ext)
    
    if not read_function:
        raise NotImplementedError(f'Cannot read image of type {ext}')
    
    return read_function(filepath, *args, **kwargs)