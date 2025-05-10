import os
import numpy as np
from pyjacket.core.slices import slice_length


class Metadata:

    def __init__(self, file_path):
        self.file_path = file_path

    @property
    def shape(self):
        """Size of each dimension (pixels)"""
        raise NotImplementedError()

    @property
    def bits(self):
        """Data format, e.g. 8bit or 12bit"""
        raise NotImplementedError()

    @property
    def resolution(self):
        """Size of each dimension (real units)"""
        raise NotImplementedError()

    @property
    def resolution_unit(self):
        """Resolution units (e.g. (ms, um, um, -))"""
        raise NotImplementedError() 

    @property
    def dict(self):
        raise NotImplementedError() 

    def __repr__(self):
        return f"Metadata({dir(self)})"


class ImageHandle:
    """Access image data lazily with numpy-like slicing"""

    slices: list[slice]
    operator: object

    def __init__(self, file_path, unzip=1):
        # print(f'Reading {unzip = }')
        self.file_path = file_path
        self.unzip = unzip
        self.data = self.open()
        # self.meta = self.get_meta()
        self.max_shape = self.get_max_shape()
        self.slices = [slice(None, None, None)] * len(self.max_shape)
        self.operator = None

        self.dtype = self.get(0).dtype

    # == IMPLEMENT THIS YOURSELF == #
    def open(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def get(self, i: int) -> np.ndarray:
        raise NotImplementedError()

    def get_max_shape(self):
        raise NotImplementedError()


    # ============================= #
    @property
    def ndim(self):
        return len(self.shape)

    @property
    def shape(self):
        """The shape of a cropped variant of this data"""
        return tuple(slice_length(s, n) for s, n in zip(self.slices, self.max_shape))

    def copy(self):
        return type(self)(self.file_path, unzip=self.unzip)

    def __del__(self):
        """Ensure all files are closed when the object is deleted."""
        self.close()

    def __getitem__(self, val):
        if not all(x == slice(None, None, None) for x in self.slices):
            raise NotImplementedError(f'slices of slices are not supported!')

        if isinstance(val, int):
            return self.get(val)

        elif isinstance(val, slice):
            obj = self.copy()
            obj.slices[0] = val
            return obj

        elif isinstance(val, tuple):
            obj = self.copy()
            obj.slices = self.slices[:]
            for i, s in enumerate(val):
                if s != slice(None, None, None):
                    obj.slices[i] = s
            return obj

    def __iter__(self):
        """Return image data frame by frame"""
        start, stop, step = self.slices[0].indices(self.max_shape[0])
        for i in range(start, stop, step):
            if self.operator:
                frame = self.operator(self, i)
            else:
                frame = self.get(i)
            frame = frame[tuple(self.slices[1:])]
            yield frame

    def __len__(self):
        return self.shape[0]

    def __repr__(self):
        base_name = os.path.basename(self.file_path)
        return f'{type(self).__name__}({base_name})'


class ImageReader:
    def read(self, file_path: str, **kwargs) -> np.ndarray:
        raise NotImplementedError()

    def read_lazy(self, file_path: str, **kwargs) -> ImageHandle:
        raise NotImplementedError()

    def seq_read(self, file_path: str, **kwargs) -> np.ndarray:
        raise NotImplementedError()

    def seq_read_lazy(self, file_path: str, **kwargs) -> ImageHandle:
        raise NotImplementedError()


    def read_meta(self, file_path: str, **kwargs) -> Metadata:
        raise NotImplementedError()


    def write(self, file_path: str, data: np.ndarray, meta:Metadata=None, **kwargs):
        raise NotImplementedError()

    def write_lazy(self, file_path: str, data: ImageHandle, meta:Metadata=None, **kwargs):
        raise NotImplementedError()


class ExifTag:
    name: None 
    value: None




