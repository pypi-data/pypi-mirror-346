import numpy as np
import os
from typing import Union, Callable, Type
from .models import Metadata
from .models import ImageHandle
from . import _mp4, _tif, _nd2, _avi, _png, _jpg
from .._path import iter_dir

"""Convention:
All arrays must be of shape
 -    (y, x)
 - (t, y, x)     (default) or (z, y, x)
 - (t, y, x, ch) (default) or (z, y, x, ch)
"""

# Each module must provide: 
class FileType:
    def read(self, file_path, **kwargs) -> np.ndarray: ...
    def read_lazy(self, file_path, **kwargs) -> ImageHandle: ...
    def seq_read(self, file_path, **kwargs) -> np.ndarray: ...
    def seq_read_lazy(self, file_path, **kwargs) -> ImageHandle: ...
    def write(self): ...
    def write_lazy(self): ...
    def read_meta(self) -> Metadata: ...

SUPPORTED: dict[str, FileType] = {
    'tif': _tif.TifReader(),
    'mp4': _mp4.MP4Reader(),
}

def read_img(file_path: str, lazy=False, **kwargs):
    """Read image data from file.

    Args:
        filepath (str): Location of the image file
        lazy (bool, optional): Read lazy to save memory. Defaults to False.

    Raises:
        ValueError: _description_
        NotImplementedError: _description_

    Returns:
        np.ndarray (default) or ImageHandle (if lazy): pixel data
    """

    # Reading folder of files?
    img_seq = os.path.isdir(file_path)

    # Obtain image extension
    pth = next(iter_dir(file_path)) if img_seq else file_path
    ext = _get_extension(pth)  ##os.path.splitext(pth)[1].lstrip('.')
    assert ext, ValueError('File ext not found in path')

    if img_seq:
        print(f'read_img: Attempting to read folder.')
        if lazy:
            reader = {
                'tif': _tif.MMStack,
            }.get(ext)
            assert reader, NotImplementedError(f'Cannot lazy-read {ext} sequence')  
            img_data: ImageHandle = reader(file_path, **kwargs)
            return img_data

        elif not lazy:
            reader = {
                # 'tif': _tif.MMStack,
            }.get(ext)
            assert reader, NotImplementedError(f'Cannot read {ext} sequence')
            img_data: np.ndarray = reader(file_path, **kwargs)
            return img_data

    else:
        if lazy:
            reader = {
                'tif': _tif.TifImageHandle,
            }.get(ext)
            assert reader, NotImplementedError(f'Cannot lazy-read {ext}')  
            img_data: ImageHandle = reader(file_path, **kwargs)
            return img_data
    
        elif not lazy:
            reader = {
                'tif': _tif.read,
            }.get(ext)
            assert reader, NotImplementedError(f'Cannot read {ext}')
            img_data: np.ndarray = reader(file_path, **kwargs)
            return img_data
        
def read_img(file_path: str, lazy=False, **kwargs):
    """Read image data from file.

    Args:
        filepath (str): Location of the image file
        lazy (bool, optional): Read lazy to save memory. Defaults to False.

    Raises:
        ValueError: _description_
        NotImplementedError: _description_

    Returns:
        np.ndarray (default) or ImageHandle (if lazy): pixel data
    """

    # Reading folder of files?
    img_seq = os.path.isdir(file_path)

    # Obtain image extension
    pth = next(iter_dir(file_path)) if img_seq else file_path
    file_type = _get_extension(pth)  ##os.path.splitext(pth)[1].lstrip('.')
    assert file_type, ValueError('File ext not found in path')
    assert file_type in SUPPORTED, NotImplementedError(f"Unsupported file type: '{file_type}'")

    lib = SUPPORTED[file_type]  # reader lib for this file type
    if img_seq:
        if lazy:  return lib.seq_read_lazy(file_path, **kwargs)
        else:     return lib.seq_read(     file_path, **kwargs)
    else:
        if lazy:  return lib.read_lazy(file_path, **kwargs)
        else:     return lib.read(     file_path, **kwargs)

def read_img_meta(file_path: str, **kwargs):
    file_type = _get_extension(file_path)
    assert file_type, ValueError('File ext not found in path')
    assert file_type in SUPPORTED, NotImplementedError(f"Unsupported file extension: '{file_type}'")

    lib = SUPPORTED[file_type]  # reader lib for this file type
    return lib.read_meta(file_path, **kwargs)

def write_img(file_path: str, data: Union[np.ndarray, ImageHandle], meta: Metadata=None, **kwargs):
    """Write image data. Supports tif, nd2"""
    # Writing as file sequence (folder of files) is not supported

    file_type = _get_extension(file_path)
    assert file_type, ValueError('File ext not found in path')
    assert file_type in SUPPORTED, NotImplementedError(f"Unsupported file type: '{file_type}'")
    
    lib = SUPPORTED[file_type]  # reader lib for this file type
    return lib.write(file_path, data, meta, **kwargs)

def _get_extension(file_path: str):
    ext = os.path.splitext(file_path)[1].lstrip('.')
    return ext

...