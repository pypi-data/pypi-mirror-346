"""Grids are graphs represented as a binary image"""

import numpy as np
from scipy.ndimage import convolve
from scipy.spatial import distance
import networkx as nx

NEIGHBOR_OFFSETS = [(-1, -1), (-1,  0), (-1,  1), 
                    ( 0, -1),           ( 0,  1), 
                    ( 1, -1), ( 1,  0), ( 1,  1)]

def graph_from_grid(skeleton: np.ndarray):
    """Convert a binary image into a graph
    
    """
    assert skeleton.dtype == np.uint8, ValueError('Skeleton must be np.uint8')
    pixel_positions = set(zip(*np.where(skeleton > 0)))
    
    graph = nx.Graph()
    for pos in pixel_positions:
        for neighbor in neighbor_positions(*pos, filter=pixel_positions):
            graph.add_edge(pos, neighbor, weight=distance.euclidean(pos, neighbor))
    return graph

def neighbor_positions(r, c, filter=None):
    """Find all neighboring coordinates.
    Optionally, return only coordinates that are present in the filter
    """
    for dr, dc in NEIGHBOR_OFFSETS:
        neighbor = (r + dr, c + dc)
        if filter is not None and neighbor not in filter:
            continue
        yield neighbor














