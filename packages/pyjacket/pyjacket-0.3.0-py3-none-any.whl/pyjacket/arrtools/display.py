import numpy as np
from math import log

from .arrtools import format_bytes

def intel(movie: np.ndarray, title=None) -> None:
    """Print a summary of imarray properties"""
    size, unit = format_bytes(movie.size * movie.itemsize)
    print("\n".join((
        f"\n=== {title or ''} (intel) ===",
        f"movie shape: {movie.shape},  [dtype: {movie.dtype}]",
        f"intensity range: {movie.min()} - {movie.max()}",
        f"memory: {size:.2f} {unit}",
    )))


# def format_bytes(n_bytes: float):
#     """Format a number of bytes such as 1024 Bytes -> 1 KB"""
#     if n_bytes < 0: raise ValueError('File size cannot be negative.')
    
#     units = ['Bytes', 'KB', 'MB', 'GB', 'TB']
#     order = int(log(n_bytes, 1024)) if n_bytes else 0
#     order = min(order, len(units)-1)  # units cant go beyond TB
#     size = n_bytes / (1024**order)
#     return size, units[order]